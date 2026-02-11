#!/usr/bin/env python3
"""
Keyword Detector Hook (UserPromptSubmit)

Detects magic keywords in user prompts and routes to appropriate skills.
Equivalent to oh-my-claudecode's keyword-detector.mjs but for Factory Droid.

Supported keywords (priority order):
1. cancelomd/stopomd: Cancel active modes
2. ralph: Persistent execution with verify/fix loops
3. autopilot: Full autonomous execution
4. ultrawork/ulw: Maximum parallel execution
5. ecomode/eco: Token-efficient execution
6. pipeline: Sequential staged execution
7. plan: Planning mode
8. research: Research orchestration
"""

import json
import sys
import re
import os
from pathlib import Path
from datetime import datetime


def read_stdin():
    try:
        return sys.stdin.read()
    except Exception:
        return ""


def extract_prompt(input_str):
    try:
        data = json.loads(input_str)
        if "prompt" in data:
            return data["prompt"]
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        return ""
    except Exception:
        return ""


def sanitize_for_detection(text):
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"`[^`]+`", "", text)
    text = re.sub(r"https?://\S+", "", text)
    return text


def activate_state(directory, prompt, state_name, session_id=""):
    state = {
        "active": True,
        "started_at": datetime.now().isoformat(),
        "original_prompt": prompt,
        "session_id": session_id or None,
        "reinforcement_count": 0,
        "last_checked_at": datetime.now().isoformat(),
    }

    if session_id:
        session_dir = Path(directory) / ".omd" / "state" / "sessions" / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        (session_dir / f"{state_name}-state.json").write_text(
            json.dumps(state, indent=2)
        )
        return

    local_dir = Path(directory) / ".omd" / "state"
    local_dir.mkdir(parents=True, exist_ok=True)
    (local_dir / f"{state_name}-state.json").write_text(json.dumps(state, indent=2))


def clear_state_files(directory, mode_names, session_id=""):
    for name in mode_names:
        paths = [
            Path(directory) / ".omd" / "state" / f"{name}-state.json",
            Path.home() / ".omd" / "state" / f"{name}-state.json",
        ]
        if session_id:
            paths.append(
                Path(directory)
                / ".omd"
                / "state"
                / "sessions"
                / session_id
                / f"{name}-state.json"
            )
        for p in paths:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


def create_skill_invocation(skill_name, original_prompt):
    return f"""[MAGIC KEYWORD: {skill_name.upper()}]

You MUST invoke the skill using the Skill tool:

Skill: oh-my-droid:{skill_name}

User request:
{original_prompt}

IMPORTANT: Invoke the skill IMMEDIATELY. Do not proceed without loading the skill instructions."""


def create_multi_skill_invocation(skills, original_prompt):
    if len(skills) == 0:
        return ""
    if len(skills) == 1:
        return create_skill_invocation(skills[0]["name"], original_prompt)

    blocks = []
    for i, s in enumerate(skills):
        blocks.append(
            f"### Skill {i + 1}: {s['name'].upper()}\nSkill: oh-my-droid:{s['name']}"
        )

    names = ", ".join(s["name"].upper() for s in skills)
    skill_blocks = "\n\n".join(blocks)

    return f"""[MAGIC KEYWORDS DETECTED: {names}]

You MUST invoke ALL of the following skills using the Skill tool, in order:

{skill_blocks}

User request:
{original_prompt}

IMPORTANT: Invoke ALL skills listed above. Start with the first skill IMMEDIATELY."""


def create_hook_output(additional_context):
    return {
        "continue": True,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        },
    }


def resolve_conflicts(matches):
    names = [m["name"] for m in matches]

    if "cancel" in names:
        return [m for m in matches if m["name"] == "cancel"]

    resolved = list(matches)

    if "ecomode" in names and "ultrawork" in names:
        resolved = [m for m in resolved if m["name"] != "ultrawork"]

    priority_order = [
        "cancel",
        "ralph",
        "autopilot",
        "ultrawork",
        "ecomode",
        "pipeline",
        "plan",
        "research",
    ]
    resolved.sort(
        key=lambda m: (
            priority_order.index(m["name"])
            if m["name"] in priority_order
            else len(priority_order)
        )
    )

    return resolved


def main():
    try:
        input_str = read_stdin()
        if not input_str.strip():
            print(json.dumps({"continue": True, "suppressOutput": True}))
            return

        data = {}
        try:
            data = json.loads(input_str)
        except Exception:
            pass

        directory = data.get("cwd", data.get("directory", os.getcwd()))
        session_id = data.get("session_id", data.get("sessionId", ""))

        prompt = extract_prompt(input_str)
        if not prompt:
            print(json.dumps({"continue": True, "suppressOutput": True}))
            return

        clean = sanitize_for_detection(prompt).lower()

        matches = []

        # Cancel
        if re.search(r"\b(cancelomd|stopomd)\b", clean):
            matches.append({"name": "cancel"})

        # Ralph
        if re.search(r"\b(ralph|don't stop|must complete|until done)\b", clean):
            matches.append({"name": "ralph"})

        # Autopilot
        if re.search(
            r"\b(autopilot|auto pilot|auto-pilot|autonomous|full auto|fullsend)\b",
            clean,
        ) or re.search(
            r"\bbuild\s+me\s+|\bcreate\s+me\s+|\bmake\s+me\s+|\bi\s+want\s+a\s+|\bhandle\s+it\s+all\b|\bend\s+to\s+end\b",
            clean,
        ):
            matches.append({"name": "autopilot"})

        # Ultrawork
        if re.search(r"\b(ultrawork|ulw|uw)\b", clean):
            matches.append({"name": "ultrawork"})

        # Ecomode
        if re.search(r"\b(eco|ecomode|eco-mode|efficient|save-tokens|budget)\b", clean):
            matches.append({"name": "ecomode"})

        # Pipeline
        if re.search(r"\b(pipeline)\b", clean) or re.search(
            r"\bchain\s+droids\b", clean
        ):
            matches.append({"name": "pipeline"})

        # Plan
        if re.search(r"\b(plan this|plan the)\b", clean):
            matches.append({"name": "plan"})

        # Research
        if re.search(r"\b(research)\b", clean):
            matches.append({"name": "research"})

        if not matches:
            print(json.dumps({"continue": True, "suppressOutput": True}))
            return

        # Deduplicate
        seen = set()
        unique = []
        for m in matches:
            if m["name"] not in seen:
                seen.add(m["name"])
                unique.append(m)

        resolved = resolve_conflicts(unique)

        # Handle cancel
        if resolved and resolved[0]["name"] == "cancel":
            clear_state_files(
                directory,
                ["ralph", "autopilot", "ultrawork", "ecomode", "pipeline"],
                session_id,
            )
            print(
                json.dumps(
                    create_hook_output(create_skill_invocation("cancel", prompt))
                )
            )
            return

        # Activate states
        state_modes = [
            m
            for m in resolved
            if m["name"] in ["ralph", "autopilot", "ultrawork", "ecomode"]
        ]
        for mode in state_modes:
            activate_state(directory, prompt, mode["name"], session_id)

        # Ralph auto-enables ultrawork
        has_ralph = any(m["name"] == "ralph" for m in resolved)
        has_ecomode = any(m["name"] == "ecomode" for m in resolved)
        has_ultrawork = any(m["name"] == "ultrawork" for m in resolved)
        if has_ralph and not has_ecomode and not has_ultrawork:
            activate_state(directory, prompt, "ultrawork", session_id)

        print(
            json.dumps(
                create_hook_output(
                    create_multi_skill_invocation(resolved, prompt)
                )
            )
        )

    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))


if __name__ == "__main__":
    main()
