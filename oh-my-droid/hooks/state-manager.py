#!/usr/bin/env python3
"""
State Manager for oh-my-droid

Manages task state with embedded spec and routing info.
Agents can read/write state via environment variables or direct file access.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

STATE_DIR = Path.home() / '.factory' / '.omd' / 'state'


class StateManager:
    """Manages task state with spec and routing integration"""
    
    def __init__(self):
        """Initialize state directory"""
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_state_path(self, key: str) -> Path:
        """Get state file path"""
        return STATE_DIR / f"{key}.json"
    
    def create_task(self, prompt: str, routing: Dict[str, Any]) -> str:
        """
        Create new task with routing information
        
        Args:
            prompt: User's task description
            routing: Router's decision (agent, autonomy, confidence, reason)
        
        Returns:
            task_id: Unique task identifier
        """
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        state = {
            "id": task_id,
            "prompt": prompt,
            "routing": routing,              # Embedded router decision
            "spec": None,                       # Filled by agent
            "status": "pending",
            "progress": 0,
            "result": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": None,
            "started_at": None,
            "completed_at": None,
        }
        
        self.save(f"tasks/{task_id}", state)
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task state by ID"""
        path = self._get_state_path(f"tasks/{task_id}")
        if path.exists():
            return json.loads(path.read_text())
        return None
    
    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update task state"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        task.update(updates)
        task["updated_at"] = datetime.now().isoformat()
        
        # Auto-update timestamps based on status
        if updates.get("status") == "executing" and not task.get("started_at"):
            task["started_at"] = datetime.now().isoformat()
        if updates.get("status") in ["completed", "error"]:
            task["completed_at"] = datetime.now().isoformat()
        
        self.save(f"tasks/{task_id}", task)
        return True
    
    def update_progress(self, task_id: str, progress: int, message: Optional[str] = None):
        """Update task progress"""
        return self.update_task(task_id, {
            "progress": progress,
            "last_message": message,
            "last_message_at": datetime.now().isoformat() if message else None
        })
    
    def complete_task(self, task_id: str, result: str, error: Optional[str] = None):
        """Mark task as completed"""
        updates = {
            "status": "completed" if not error else "error",
            "result": result,
            "progress": 100,
            "completed_at": datetime.now().isoformat()
        }
        if error:
            updates["error"] = error
        
        return self.update_task(task_id, updates)
    
    def set_task_agent(self, task_id: str, agent: str, spec: str):
        """Agent updates its spec in state"""
        return self.update_task(task_id, {
            "agent": agent,
            "spec": spec,
            "status": "executing" if not self.get_task(task_id).get("started_at") else "pending"
        })
    
    def save(self, key: str, data: Dict[str, Any]):
        """Save state to file"""
        path = self._get_state_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """Load state from file"""
        path = self._get_state_path(key)
        if path.exists():
            return json.loads(path.read_text())
        return None
    
    def get_session_tasks(self, session_id: Optional[str] = None) -> list:
        """Get all tasks, optionally filtered by session"""
        tasks = []
        for file in STATE_DIR.glob("tasks/*.json"):
            try:
                task = json.loads(file.read_text())
                if session_id is None or task.get("session_id") == session_id:
                    tasks.append(task)
            except (json.JSONDecodeError, KeyError):
                continue
        return tasks
    
    def get_pending_tasks(self) -> list:
        """Get all pending tasks"""
        return [t for t in self.get_session_tasks() if t.get("status") in ["pending", "executing"]]
    
    def cleanup_old_tasks(self, max_age_hours: int = 24) -> int:
        """Remove completed tasks older than max_age_hours"""
        import time
        now = time.time()
        removed = 0
        
        for file in STATE_DIR.glob("tasks/*.json"):
            try:
                task = json.loads(file.read_text())
                if task.get("status") in ["completed", "error"]:
                    completed_at = task.get("completed_at")
                    if completed_at:
                        from datetime import datetime
                        dt = datetime.fromisoformat(completed_at)
                        age_hours = (now - dt.timestamp()) / 3600
                        if age_hours > max_age_hours:
                            file.unlink()
                            removed += 1
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
        
        return removed
    
    def get_current_task_id(self) -> Optional[str]:
        """Get task ID from environment (for agent use)"""
        return os.getenv("STATE_TASK_ID")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get state summary"""
        tasks = self.get_session_tasks()
        return {
            "total": len(tasks),
            "pending": len([t for t in tasks if t.get("status") == "pending"]),
            "executing": len([t for t in tasks if t.get("status") == "executing"]),
            "completed": len([t for t in tasks if t.get("status") == "completed"]),
            "error": len([t for t in tasks if t.get("status") == "error"]),
            "state_dir": str(STATE_DIR)
        }


def load_hook_input() -> Dict[str, Any]:
    """Load hook input from stdin"""
    return json.load(sys.stdin)


def output_json(data: Dict[str, Any]) -> None:
    """Output JSON to stdout"""
    print(json.dumps(data, indent=2))


def cmd_create(args: list) -> None:
    """Create new task"""
    if len(args) < 3:
        output_json({"error": "Usage: create <prompt> <agent> <autonomy> [reason] [confidence]"})
        sys.exit(1)
    
    prompt = args[0]
    routing = {
        "agent": args[1],
        "autonomy": args[2],
        "reason": args[3] if len(args) > 3 else "Manual assignment",
        "confidence": float(args[4]) if len(args) > 4 else 1.0
    }
    
    manager = StateManager()
    task_id = manager.create_task(prompt, routing)
    
    output_json({
        "task_id": task_id,
        "routing": routing,
        "status": "created"
    })


def cmd_update(args: list) -> None:
    """Update task"""
    if len(args) < 2:
        output_json({"error": "Usage: update <task_id> <key>=<value>..."})
        sys.exit(1)
    
    task_id = args[0]
    updates = {}
    
    for arg in args[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            updates[key] = value
    
    manager = StateManager()
    success = manager.update_task(task_id, updates)
    
    output_json({
        "task_id": task_id,
        "success": success
    })


def cmd_get(args: list) -> None:
    """Get task"""
    if len(args) < 1:
        output_json({"error": "Usage: get <task_id>"})
        sys.exit(1)
    
    task_id = args[0]
    manager = StateManager()
    task = manager.get_task(task_id)
    
    if task:
        output_json(task)
    else:
        output_json({"error": f"Task not found: {task_id}"})


def cmd_list(args: list) -> None:
    """List all tasks"""
    manager = StateManager()
    tasks = manager.get_session_tasks()
    summary = manager.get_summary()
    
    output_json({
        "summary": summary,
        "tasks": tasks
    })


def cmd_cleanup(args: list) -> None:
    """Cleanup old tasks"""
    max_hours = int(args[0]) if len(args) > 0 else 24
    manager = StateManager()
    removed = manager.cleanup_old_tasks(max_hours)
    
    output_json({
        "cleaned": True,
        "removed_count": removed
    })


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        manager = StateManager()
        output_json(manager.get_summary())
        sys.exit(0)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "create": cmd_create,
        "update": cmd_update,
        "get": cmd_get,
        "list": cmd_list,
        "cleanup": cmd_cleanup,
        "summary": lambda args: output_json(StateManager().get_summary()),
    }
    
    if command in commands:
        commands[command](args)
    else:
        output_json({"error": f"Unknown command: {command}", "available": list(commands.keys())})
        sys.exit(1)


if __name__ == "__main__":
    main()
