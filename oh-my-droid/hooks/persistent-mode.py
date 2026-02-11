#!/usr/bin/env python3
"""
Persistent Mode Hook (Stop)

Prevents the session from stopping when persistent modes are active.
Re-injects continuation prompts for ralph, autopilot, ultrawork, etc.
Equivalent to oh-my-claudecode's persistent-mode.cjs.

Supported modes: ralph, autopilot, ultrawork, ecomode, pipeline
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime


STALE_THRESHOLD_HOURS = 2


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


def write_json_file(path, data):
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, indent=2))
        return True
    except Exception:
        return False


def is_stale_state(state):
    if not state:
        return True

    last_checked = state.get("last_checked_at", "")
    started_at = state.get("started_at", "")

    try:
        times = []
        if last_checked:
            times.append(datetime.fromisoformat(last_checked.replace("Z", "+00:00")))
        if started_at:
            times.append(datetime.fromisoformat(started_at.replace("Z", "+00:00")))

        if not times:
            return True

        most_recent = max(times)
        age_hours = (
            datetime.now(most_recent.tzinfo or None) - most_recent
        ).total_seconds() / 3600

        return age_hours > STALE_THRESHOLD_HOURS
    except Exception:
        return True


def get_state_path(directory, mode_name, session_id=""):
    if session_id:
        return (
            Path(directory)
            / ".omd"
            / "state"
            / "sessions"
            / session_id
            / f"{mode_name}-state.json"
        )
    return Path(directory) / ".omd" / "state" / f"{mode_name}-state.json"


def get_active_modes(directory, session_id=""):
    modes = ["ralph", "autopilot", "ultrawork", "ecomode", "pipeline"]
    active = []

    for mode in modes:
        state = read_json_file(get_state_path(directory, mode, session_id))
        if not state:
            state = read_json_file(get_state_path(directory, mode))

        if state and state.get("active") and not is_stale_state(state):
            active.append({"name": mode, "state": state})

    return active


def generate_continuation(active_modes, directory, session_id):
    if not active_modes:
        return None

    mode_names = [m["name"] for m in active_modes]

    messages = []
    for mode in active_modes:
        name = mode["name"]
        state = mode["state"]
        prompt = state.get("original_prompt", "Task in progress")
        count = state.get("reinforcement_count", 0) + 1

        # Update reinforcement count
        state["reinforcement_count"] = count
        state["last_checked_at"] = datetime.now().isoformat()
        state_path = get_state_path(directory, name, session_id)
        write_json_file(str(state_path), state)

        if name == "ralph":
            messages.append(
                f"[RALPH MODE ACTIVE - Reinforcement #{count}]\n"
                f"Task: {prompt}\n"
                f"You MUST continue working. Do NOT stop until the task is verified complete.\n"
                f"If blocked, try a different approach. Max 3 fix attempts per issue."
            )
        elif name == "autopilot":
            messages.append(
                f"[AUTOPILOT MODE ACTIVE - Reinforcement #{count}]\n"
                f"Task: {prompt}\n"
                f"Continue autonomous execution. Plan, execute, review, fix - all automatically.\n"
                f"Do NOT stop until the task is fully complete."
            )
        elif name == "ultrawork":
            messages.append(
                f"[ULTRAWORK MODE ACTIVE - Reinforcement #{count}]\n"
                f"Task: {prompt}\n"
                f"Continue parallel execution. Launch droids for independent subtasks.\n"
                f"Do NOT stop until all subtasks are complete."
            )
        elif name == "ecomode":
            messages.append(
                f"[ECOMODE ACTIVE]\n"
                f"Task: {prompt}\n"
                f"Continue with token-efficient execution."
            )
        elif name == "pipeline":
            messages.append(
                f"[PIPELINE MODE ACTIVE]\n"
                f"Task: {prompt}\n"
                f"Continue with next pipeline stage."
            )

    combined = "\n\n---\n\n".join(messages)
    return (
        f"<persistent-mode>\n\n"
        f"Active modes: {', '.join(mode_names)}\n\n"
        f"{combined}\n\n"
        f"IMPORTANT: Do NOT stop. Continue working on the task.\n\n"
        f"</persistent-mode>"
    )


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

        active_modes = get_active_modes(directory, session_id)

        if not active_modes:
            print(json.dumps({"continue": True, "suppressOutput": True}))
            return

        continuation = generate_continuation(active_modes, directory, session_id)

        if continuation:
            print(
                json.dumps(
                    {
                        "continue": True,
                        "hookSpecificOutput": {
                            "hookEventName": "Stop",
                            "additionalContext": continuation,
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
