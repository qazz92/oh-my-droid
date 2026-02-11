#!/usr/bin/env python3
"""
PostToolUse Hook: Verification Reminder System

Monitors tool execution results and provides contextual guidance.
Tracks session statistics and detects failures.
Equivalent to oh-my-claudecode's post-tool-verifier.mjs.
"""

import json
import sys
import os
import re
from pathlib import Path


def read_stdin():
    try:
        return sys.stdin.read()
    except Exception:
        return ""


STATE_FILE = Path.home() / ".factory" / ".session-stats.json"


def load_stats():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except Exception:
        pass
    return {"sessions": {}}


def save_stats(stats):
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(stats, indent=2))
    except Exception:
        pass


def update_stats(tool_name, session_id):
    stats = load_stats()
    if session_id not in stats["sessions"]:
        stats["sessions"][session_id] = {
            "tool_counts": {},
            "last_tool": "",
            "total_calls": 0,
        }
    session = stats["sessions"][session_id]
    session["tool_counts"][tool_name] = session["tool_counts"].get(tool_name, 0) + 1
    session["last_tool"] = tool_name
    session["total_calls"] = session.get("total_calls", 0) + 1
    save_stats(stats)
    return session["tool_counts"][tool_name]


ERROR_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"error:",
        r"failed",
        r"cannot",
        r"permission denied",
        r"command not found",
        r"no such file",
        r"exit code: [1-9]",
        r"fatal:",
        r"abort",
    ]
]

BG_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [r"started", r"running", r"background", r"task_id", r"spawned"]
]


def detect_failure(output):
    return any(p.search(output) for p in ERROR_PATTERNS)


def detect_background(output):
    return any(p.search(output) for p in BG_PATTERNS)


def get_droid_summary(directory):
    tracking_file = Path(directory) / ".omd" / "state" / "subagent-tracking.json"
    try:
        if tracking_file.exists():
            data = json.loads(tracking_file.read_text())
            agents = data.get("agents", [])
            running = [a for a in agents if a.get("status") == "running"]
            completed = data.get("total_completed", 0)
            failed = data.get("total_failed", 0)
            if not running and completed == 0 and failed == 0:
                return ""
            parts = []
            if running:
                names = ", ".join(
                    a.get("agent_type", "?").replace("oh-my-droid:", "")
                    for a in running
                )
                parts.append(f"Running: {len(running)} [{names}]")
            if completed > 0:
                parts.append(f"Completed: {completed}")
            if failed > 0:
                parts.append(f"Failed: {failed}")
            return " | ".join(parts)
    except Exception:
        pass
    return ""


def generate_message(tool_name, tool_output, tool_count, directory):
    message = ""

    if tool_name == "Execute":
        if detect_failure(tool_output):
            message = "Command failed. Please investigate the error and fix before continuing."
        elif detect_background(tool_output):
            message = "Background operation detected. Remember to verify results before proceeding."

    elif tool_name == "Task":
        droid_summary = get_droid_summary(directory)
        if detect_failure(tool_output):
            message = "Task delegation failed. Verify droid name and parameters."
        elif detect_background(tool_output):
            message = "Background task launched. Check results when needed."
        elif tool_count > 5:
            message = f"Multiple tasks delegated ({tool_count} total). Track their completion status."
        if droid_summary:
            message = f"{message} | {droid_summary}" if message else droid_summary

    elif tool_name in ("Edit", "MultiEdit"):
        if detect_failure(tool_output):
            message = "Edit operation failed. Verify file exists and content matches exactly."
        else:
            message = "Code modified. Verify changes work as expected before marking complete."

    elif tool_name == "Create":
        if detect_failure(tool_output):
            message = "Write operation failed. Check file permissions and directory existence."
        else:
            message = "File written. Test the changes to ensure they work correctly."

    elif tool_name == "TodoWrite":
        if re.search(r"created|added", tool_output, re.IGNORECASE):
            message = "Todo list updated. Proceed with next task on the list."
        elif re.search(r"completed|done", tool_output, re.IGNORECASE):
            message = "Task marked complete. Continue with remaining todos."
        elif re.search(r"in_progress", tool_output, re.IGNORECASE):
            message = "Task marked in progress. Focus on completing this task."

    elif tool_name == "Read":
        if tool_count > 10:
            message = f"Extensive reading ({tool_count} files). Consider using Grep for pattern searches."

    elif tool_name == "Grep":
        if re.search(r"^0$|no matches", tool_output, re.IGNORECASE):
            message = "No matches found. Verify pattern syntax or try broader search."

    return message


def main():
    try:
        input_str = read_stdin()
        data = json.loads(input_str)

        tool_name = data.get("tool_name", data.get("toolName", ""))
        raw_response = data.get("tool_response", data.get("toolOutput", ""))
        tool_output = (
            raw_response if isinstance(raw_response, str) else json.dumps(raw_response)
        )
        session_id = data.get("session_id", data.get("sessionId", "unknown"))
        directory = data.get("cwd", data.get("directory", os.getcwd()))

        tool_count = update_stats(tool_name, session_id)
        message = generate_message(tool_name, tool_output, tool_count, directory)

        response = {"continue": True}
        if message:
            response["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": message,
            }
        else:
            response["suppressOutput"] = True

        print(json.dumps(response))

    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))


if __name__ == "__main__":
    main()
