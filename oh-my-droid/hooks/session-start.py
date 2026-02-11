#!/usr/bin/env python3
"""
Session Start Hook (SessionStart)

Restores persistent mode states when a new session begins.
Checks for active ralph/ultrawork/autopilot states and pending todos.
Equivalent to oh-my-claudecode's session-start.mjs.
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


def read_json_file(path):
    try:
        p = Path(path)
        if p.exists():
            return json.loads(p.read_text())
    except Exception:
        pass
    return None


def main():
    try:
        input_str = read_stdin()
        data = {}
        try:
            data = json.loads(input_str)
        except Exception:
            pass

        directory = data.get("cwd", data.get("directory", os.getcwd()))
        session_id = data.get("session_id", data.get("sessionId", ""))
        messages = []

        # Check ultrawork state
        ultrawork_state = None
        if session_id:
            ultrawork_state = read_json_file(
                Path(directory)
                / ".omd"
                / "state"
                / "sessions"
                / session_id
                / "ultrawork-state.json"
            )
            if (
                ultrawork_state
                and ultrawork_state.get("session_id")
                and ultrawork_state["session_id"] != session_id
            ):
                ultrawork_state = None
        else:
            ultrawork_state = read_json_file(
                Path(directory) / ".omd" / "state" / "ultrawork-state.json"
            )

        if ultrawork_state and ultrawork_state.get("active"):
            messages.append(
                f"""<session-restore>

[ULTRAWORK MODE RESTORED]

You have an active ultrawork session from {ultrawork_state.get('started_at', 'unknown')}.
Original task: {ultrawork_state.get('original_prompt', 'Task in progress')}

Continue working in ultrawork mode until all tasks are complete.

</session-restore>

---
"""
            )

        # Check ralph state
        ralph_state = None
        if session_id:
            ralph_state = read_json_file(
                Path(directory)
                / ".omd"
                / "state"
                / "sessions"
                / session_id
                / "ralph-state.json"
            )
            if (
                ralph_state
                and ralph_state.get("session_id")
                and ralph_state["session_id"] != session_id
            ):
                ralph_state = None
        else:
            ralph_state = read_json_file(
                Path(directory) / ".omd" / "state" / "ralph-state.json"
            )

        if ralph_state and ralph_state.get("active"):
            messages.append(
                f"""<session-restore>

[RALPH LOOP RESTORED]

You have an active ralph-loop session.
Original task: {ralph_state.get('original_prompt', 'Task in progress')}

Continue working until the task is verified complete.

</session-restore>

---
"""
            )

        # Check autopilot state
        autopilot_state = None
        if session_id:
            autopilot_state = read_json_file(
                Path(directory)
                / ".omd"
                / "state"
                / "sessions"
                / session_id
                / "autopilot-state.json"
            )
        else:
            autopilot_state = read_json_file(
                Path(directory) / ".omd" / "state" / "autopilot-state.json"
            )

        if autopilot_state and autopilot_state.get("active"):
            messages.append(
                f"""<session-restore>

[AUTOPILOT MODE RESTORED]

You have an active autopilot session.
Original task: {autopilot_state.get('original_prompt', 'Task in progress')}

Continue working autonomously until task completion.

</session-restore>

---
"""
            )

        # Check pending todos
        todo_paths = [
            Path(directory) / ".omd" / "todos.json",
        ]
        incomplete_count = 0
        for todo_file in todo_paths:
            state_data = read_json_file(todo_file)
            if state_data:
                todos = state_data.get("todos", state_data if isinstance(state_data, list) else [])
                incomplete_count += sum(
                    1
                    for t in todos
                    if t.get("status") not in ("completed", "cancelled")
                )

        if incomplete_count > 0:
            messages.append(
                f"""<session-restore>

[PENDING TASKS DETECTED]

You have {incomplete_count} incomplete tasks from a previous session.
Please continue working on these tasks.

</session-restore>

---
"""
            )

        if messages:
            print(
                json.dumps(
                    {
                        "continue": True,
                        "hookSpecificOutput": {
                            "hookEventName": "SessionStart",
                            "additionalContext": "\n".join(messages),
                        },
                    }
                )
            )
        else:
            print(json.dumps({"continue": True, "suppressOutput": True}))

    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))


if __name__ == "__main__":
    main()
