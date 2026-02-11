#!/usr/bin/env python3
"""
Background Manager for Factory Droid

Manages background tasks for parallel task execution.
Adapted from oh-my-claudeCode's BackgroundManager (TypeScript).

Usage:
    python background-manager.py launch <description> <prompt> <agent> <session_id>
    python background-manager.py complete <task_id> <result>
    python background-manager.py status <task_id>
    python background-manager.py list
    python background-manager.py cleanup
"""

import json
import os
import sys
import uuid
import time
from datetime import datetime
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# Constants
DEFAULT_TASK_TTL_MS = 30 * 60 * 1000  # 30 minutes
STALE_THRESHOLD_MS = 5 * 60 * 1000    # 5 minutes
BACKGROUND_TASKS_DIR = Path(os.path.expanduser("~/.factory/.omd/background-tasks"))


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass
class TaskProgress:
    tool_calls: int = 0
    last_tool: Optional[str] = None
    last_update: str = ""
    last_message: Optional[str] = None
    last_message_at: Optional[str] = None

    def __post_init__(self):
        if not self.last_update:
            self.last_update = datetime.now().isoformat()


@dataclass
class BackgroundTask:
    id: str
    session_id: str
    parent_session_id: str
    description: str
    prompt: str
    agent: str
    status: str
    started_at: str
    queued_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    progress: Optional[dict] = None
    concurrency_key: Optional[str] = None
    parent_model: Optional[str] = None

    def __post_init__(self):
        if self.progress is None:
            self.progress = {
                "toolCalls": 0,
                "lastUpdate": self.started_at
            }


@dataclass
class ResumeContext:
    session_id: str
    previous_prompt: str
    tool_call_count: int = 0
    last_tool_used: Optional[str] = None
    last_output_summary: Optional[str] = None
    started_at: str = ""
    last_activity_at: str = ""


class BackgroundManager:
    """Manages background tasks for the Sisyphus system."""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.tasks: dict[str, BackgroundTask] = {}
        self.notifications: dict[str, list[str]] = {}
        self._ensure_storage_dir()
        self._load_persisted_tasks()
    
    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists."""
        BACKGROUND_TASKS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _generate_task_id(self) -> str:
        """Generate a unique task ID."""
        timestamp = format(int(time.time() * 1000), 'x')  # 36진수
        random = uuid.uuid4().hex[:6]
        return f"bg_{timestamp}{random}"
    
    def _get_task_path(self, task_id: str) -> Path:
        """Get storage path for a task."""
        return BACKGROUND_TASKS_DIR / f"{task_id}.json"
    
    def _persist_task(self, task: BackgroundTask) -> None:
        """Persist a task to disk."""
        path = self._get_task_path(task.id)
        task_dict = asdict(task)
        # Convert datetime objects to ISO strings
        if task_dict.get('progress'):
            task_dict['progress']['lastUpdate'] = str(task_dict['progress']['lastUpdate'])
        with open(path, 'w') as f:
            json.dump(task_dict, f, indent=2)
    
    def _unpersist_task(self, task_id: str) -> None:
        """Remove persisted task from disk."""
        path = self._get_task_path(task_id)
        if path.exists():
            path.unlink()
    
    def _load_persisted_tasks(self) -> None:
        """Load persisted tasks from disk."""
        if not BACKGROUND_TASKS_DIR.exists():
            return
        
        for file in BACKGROUND_TASKS_DIR.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    task_data = json.load(f)
                
                task = BackgroundTask(**task_data)
                self.tasks[task.id] = task
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
    
    def launch(
        self,
        description: str,
        prompt: str,
        agent: str,
        parent_session_id: str,
        model: Optional[str] = None
    ) -> dict:
        """Launch a new background task and execute the agent."""
        task_id = self._generate_task_id()
        session_id = f"ses_{uuid.uuid4().hex[:12]}"
        now = datetime.now().isoformat()
        
        task = BackgroundTask(
            id=task_id,
            session_id=session_id,
            parent_session_id=parent_session_id,
            description=description,
            prompt=prompt,
            agent=agent,
            status=TaskStatus.RUNNING.value,
            started_at=now,
            concurrency_key=agent,
            parent_model=model
        )
        
        self.tasks[task_id] = task
        self._persist_task(task)
        
        # Execute the agent in background
        try:
            # Escape quotes for shell command
            escaped_prompt = prompt.replace('"', '\\"')
            cmd = [
                "droid",
                "task",
                agent,
                escaped_prompt
            ]
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except Exception as e:
            print(f"Warning: Failed to launch agent: {e}", file=sys.stderr)
        
        return {
            "taskId": task_id,
            "sessionId": session_id,
            "description": description,
            "status": task.status
        }
    
    def complete(self, task_id: str, result: str, error: Optional[str] = None) -> dict:
        """Mark a task as completed."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        task.status = TaskStatus.COMPLETED.value if not error else TaskStatus.ERROR.value
        task.completed_at = datetime.now().isoformat()
        task.result = result
        task.error = error
        
        if task.concurrency_key:
            pass  # Concurrency release handled by caller
        
        self._persist_task(task)
        
        return {
            "taskId": task_id,
            "status": task.status,
            "completed": True
        }
    
    def get_task(self, task_id: str) -> Optional[dict]:
        """Get a task by ID."""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        task_dict = asdict(task)
        task_dict['progress'] = task.progress
        return task_dict
    
    def find_by_session(self, session_id: str) -> Optional[BackgroundTask]:
        """Find a task by session ID."""
        for task in self.tasks.values():
            if task.session_id == session_id:
                return task
        return None
    
    def get_tasks_by_parent_session(self, parent_session_id: str) -> list[dict]:
        """Get all tasks for a parent session."""
        result = []
        for task in self.tasks.values():
            if task.parent_session_id == parent_session_id:
                result.append(asdict(task))
        return result
    
    def get_all_tasks(self) -> list[dict]:
        """Get all tasks."""
        return [asdict(t) for t in self.tasks.values()]
    
    def get_running_tasks(self) -> list[dict]:
        """Get all running tasks."""
        return [
            asdict(t) for t in self.tasks.values()
            if t.status == TaskStatus.RUNNING.value
        ]
    
    def get_queued_tasks(self) -> list[dict]:
        """Get all queued tasks."""
        return [
            asdict(t) for t in self.tasks.values()
            if t.status == TaskStatus.QUEUED.value
        ]
    
    def update_status(
        self,
        task_id: str,
        status: str,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """Update task status."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        task.status = status
        if result is not None:
            task.result = result
        if error is not None:
            task.error = error
        
        if status in [TaskStatus.COMPLETED.value, TaskStatus.ERROR.value, TaskStatus.CANCELLED.value]:
            task.completed_at = datetime.now().isoformat()
            self._persist_task(task)
    
    def update_progress(
        self,
        task_id: str,
        tool_calls: Optional[int] = None,
        last_tool: Optional[str] = None,
        last_message: Optional[str] = None
    ) -> None:
        """Update task progress."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task not found: {task_id}")
        
        if task.progress is None:
            task.progress = {"toolCalls": 0, "lastUpdate": datetime.now().isoformat()}
        
        if tool_calls is not None:
            task.progress["toolCalls"] = tool_calls
        if last_tool is not None:
            task.progress["lastTool"] = last_tool
        if last_message is not None:
            task.progress["lastMessage"] = last_message[:500] if last_message else None
            task.progress["lastMessageAt"] = datetime.now().isoformat()
        
        task.progress["lastUpdate"] = datetime.now().isoformat()
        self._persist_task(task)
    
    def get_resume_context(self, session_id: str) -> Optional[dict]:
        """Get resume context for a session."""
        task = self.find_by_session(session_id)
        if not task:
            return None
        
        progress = task.progress or {}
        return {
            "sessionId": task.session_id,
            "previousPrompt": task.prompt,
            "toolCallCount": progress.get("toolCalls", 0),
            "lastToolUsed": progress.get("lastTool"),
            "lastOutputSummary": progress.get("lastMessage", "")[:500] if progress.get("lastMessage") else None,
            "startedAt": task.started_at,
            "lastActivityAt": progress.get("lastUpdate", task.started_at)
        }
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task completely."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        self._unpersist_task(task_id)
        del self.tasks[task_id]
        return True
    
    def prune_stale_tasks(self) -> dict:
        """Remove stale tasks that have exceeded their TTL."""
        now = time.time() * 1000
        ttl = self.config.get("taskTimeoutMs", DEFAULT_TASK_TTL_MS)
        removed = []
        
        stale_threshold = self.config.get("staleThresholdMs", STALE_THRESHOLD_MS)
        
        tasks_to_remove = []
        for task_id, task in self.tasks.items():
            if task.status not in [TaskStatus.RUNNING.value, TaskStatus.QUEUED.value]:
                continue
            
            started = datetime.fromisoformat(task.started_at)
            age = now - started.timestamp() * 1000
            
            if age > ttl:
                tasks_to_remove.append((task_id, "timeout"))
                continue
            
            # Check for stale sessions
            if task.status == TaskStatus.RUNNING.value:
                last_update_str = task.progress.get("lastUpdate", task.started_at) if task.progress else task.started_at
                last_update = datetime.fromisoformat(last_update_str)
                inactive_time = now - last_update.timestamp() * 1000
                
                if inactive_time > stale_threshold * 2:
                    tasks_to_remove.append((task_id, "stale"))
        
        for task_id, reason in tasks_to_remove:
            task = self.tasks[task_id]
            task.status = TaskStatus.ERROR.value
            task.error = f"Task {reason}: no activity"
            task.completed_at = datetime.now().isoformat()
            self._persist_task(task)
            removed.append(task_id)
            del self.tasks[task_id]
        
        return {"removed": removed}
    
    def get_status_summary(self) -> dict:
        """Get a summary of all tasks."""
        running = self.get_running_tasks()
        queued = self.get_queued_tasks()
        all_tasks = self.get_all_tasks()
        
        return {
            "total": len(all_tasks),
            "running": len(running),
            "queued": len(queued),
            "completed": len([t for t in all_tasks if t.get("status") == TaskStatus.COMPLETED.value]),
            "error": len([t for t in all_tasks if t.get("status") == TaskStatus.ERROR.value]),
            "tasks": all_tasks
        }
    
    def cleanup(self) -> None:
        """Cleanup manager."""
        self.tasks.clear()
        self.notifications.clear()


def load_hook_input() -> dict:
    """Load hook input from stdin."""
    return json.load(sys.stdin)


def output_json(data: dict) -> None:
    """Output JSON to stdout."""
    print(json.dumps(data))


def cmd_launch(args: list[str]) -> None:
    """Launch a new background task."""
    if len(args) < 4:
        output_json({"error": "Usage: launch <description> <prompt> <agent> <parent_session_id> [model]"})
        sys.exit(1)
    
    description = args[0]
    prompt = args[1]
    agent = args[2]
    parent_session_id = args[3]
    model = args[4] if len(args) > 4 else None
    
    manager = BackgroundManager()
    result = manager.launch(description, prompt, agent, parent_session_id, model)
    output_json(result)


def cmd_complete(args: list[str]) -> None:
    """Complete a background task."""
    if len(args) < 2:
        output_json({"error": "Usage: complete <task_id> <result> [error]"})
        sys.exit(1)
    
    task_id = args[0]
    result = args[1]
    error = args[2] if len(args) > 2 else None
    
    manager = BackgroundManager()
    try:
        output_json(manager.complete(task_id, result, error))
    except ValueError as e:
        output_json({"error": str(e)})


def cmd_status(args: list[str]) -> None:
    """Get status of a task."""
    if len(args) < 1:
        output_json({"error": "Usage: status <task_id>"})
        sys.exit(1)
    
    task_id = args[0]
    manager = BackgroundManager()
    task = manager.get_task(task_id)
    
    if task:
        output_json(task)
    else:
        output_json({"error": f"Task not found: {task_id}"})


def cmd_list(args: list[str]) -> None:
    """List all tasks."""
    manager = BackgroundManager()
    output_json(manager.get_status_summary())


def cmd_prune(args: list[str]) -> None:
    """Prune stale tasks."""
    manager = BackgroundManager()
    result = manager.prune_stale_tasks()
    output_json(result)


def cmd_cleanup(args: list[str]) -> None:
    """Cleanup all tasks."""
    manager = BackgroundManager()
    manager.cleanup()
    output_json({"cleaned": True})


def cmd_hook_complete(args: list[str]) -> None:
    """Handle SubagentStop hook completion."""
    input_data = load_hook_input()
    
    session_id = input_data.get("session_id")
    transcript_path = input_data.get("transcript_path")
    
    if not session_id:
        output_json({"error": "No session_id in hook input"})
        sys.exit(0)
    
    # Try to get result from transcript
    result = None
    error = None
    
    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path, 'r') as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if line.strip():
                        msg = json.loads(line)
                        if msg.get("role") == "assistant":
                            content = msg.get("content", [])
                            for c in content:
                                if c.get("type") == "text":
                                    result = c.get("text", "")
                            break
        except Exception:
            pass
    
    manager = BackgroundManager()
    task = manager.find_by_session(session_id)
    
    if task:
        output_json(manager.complete(task.id, result or "", error))
    else:
        output_json({"error": f"Task not found for session: {session_id}"})


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "launch": cmd_launch,
        "complete": cmd_complete,
        "status": cmd_status,
        "list": cmd_list,
        "prune": cmd_prune,
        "cleanup": cmd_cleanup,
        "hook-complete": cmd_hook_complete,
    }
    
    if command in commands:
        commands[command](args)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: launch, complete, status, list, prune, cleanup, hook-complete")
        sys.exit(1)


if __name__ == "__main__":
    main()
