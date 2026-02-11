#!/usr/bin/env python3
"""
PreToolUse Hook: Contextual Reminder Enforcer

Injects contextual reminders before every tool execution.
Provides todo status and tool-specific guidance.
Equivalent to oh-my-claudecode's pre-tool-enforcer.mjs.
"""

import json
import sys
import os
from pathlib import Path


def read_stdin():
    try:
        return sys.stdin.read()
    except Exception:
        return ""


def get_todo_status(directory):
    todo_paths = [
        Path(directory) / ".omd" / "todos.json",
    ]
    pending = 0
    in_progress = 0

    for todo_file in todo_paths:
        try:
            if todo_file.exists():
                data = json.loads(todo_file.read_text())
                todos = data.get("todos", data if isinstance(data, list) else [])
                pending += sum(1 for t in todos if t.get("status") == "pending")
                in_progress += sum(
                    1 for t in todos if t.get("status") == "in_progress"
                )
        except Exception:
            pass

    if pending + in_progress > 0:
        return f"[{in_progress} active, {pending} pending] "
    return ""


def get_droid_tracking_info(directory):
    tracking_file = Path(directory) / ".omd" / "state" / "subagent-tracking.json"
    try:
        if tracking_file.exists():
            data = json.loads(tracking_file.read_text())
            agents = data.get("agents", [])
            running = sum(1 for a in agents if a.get("status") == "running")
            return {"running": running, "total": data.get("total_spawned", 0)}
    except Exception:
        pass
    return {"running": 0, "total": 0}


TOOL_MESSAGES = {
    "TodoWrite": "Mark todos in_progress BEFORE starting, completed IMMEDIATELY after finishing.",
    "Execute": "Use parallel execution for independent tasks.",
    "Edit": "Verify changes work after editing. Test functionality before marking complete.",
    "MultiEdit": "Verify changes work after editing. Test functionality before marking complete.",
    "Create": "Verify new file works as expected. Test functionality before marking complete.",
    "Read": "Read multiple files in parallel when possible for faster analysis.",
    "Grep": "Combine searches in parallel when investigating multiple patterns.",
    "Glob": "Combine searches in parallel when investigating multiple patterns.",
    "Task": "Launch multiple droids in parallel when tasks are independent.",
}


def generate_message(tool_name, todo_status, tool_input=None, directory=""):
    if tool_name == "Task":
        tracking = get_droid_tracking_info(directory)
        droid_type = "unknown"
        desc = ""
        if tool_input and isinstance(tool_input, dict):
            droid_type = tool_input.get("subagent_type", "unknown")
            desc = tool_input.get("description", "")

        parts = [f"{todo_status}Spawning droid: {droid_type}"]
        if desc:
            parts.append(f"Task: {desc}")
        if tracking["running"] > 0:
            parts.append(f"Active droids: {tracking['running']}")
        return " | ".join(parts)

    msg = TOOL_MESSAGES.get(
        tool_name, f"{todo_status}Continue until all tasks complete."
    )
    return f"{todo_status}{msg}" if todo_status and not msg.startswith("[") else msg


def main():
    try:
        input_str = read_stdin()
        data = {}
        try:
            data = json.loads(input_str)
        except Exception:
            pass

        tool_name = data.get("tool_name", data.get("toolName", "unknown"))
        directory = data.get("cwd", data.get("directory", os.getcwd()))
        tool_input = data.get("tool_input", data.get("toolInput"))

        todo_status = get_todo_status(directory)
        message = generate_message(tool_name, todo_status, tool_input, directory)

        print(
            json.dumps(
                {
                    "continue": True,
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "additionalContext": message,
                    },
                }
            )
        )

    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))


if __name__ == "__main__":
    main()
