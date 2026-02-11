---
description: Launch background tasks for parallel droid execution using background-manager.py
argument-hint: <description> <prompt>
---

You MUST invoke the **task-bg** skill using the Skill tool:

Skill: task-bg

User task: $ARGUMENTS

Task-bg uses `background-manager.py` for manual background execution (Factory Droid has no native `run_in_background`):
1. Parse description and prompt from user input
2. Select appropriate droid based on task type
3. Launch via `python3 hooks/background-manager.py launch "<desc>" "<prompt>" <droid> <session_id> [autonomy]`
4. Monitor with `python3 hooks/background-manager.py list` or `status <id>`
5. Collect results with `python3 hooks/background-manager.py output <id>`
