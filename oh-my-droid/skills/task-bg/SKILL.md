---
name: task-bg
description: Launch background tasks for parallel execution
---

# Task-bg

Launch background tasks that run in parallel.

## When to Use

- Multiple independent tasks that can run simultaneously
- Exploration, research, or analysis tasks
- Tasks where you want to continue working while background tasks run

## How It Works

This skill runs `background-manager.py` to:
1. Launch a background task using `droid exec`
2. Capture stdout to a file
3. Track task status in JSON

## Usage

```bash
python hooks/background-manager.py launch "<description>" "<prompt>" "<agent>" "<parent_session>" [autonomy_level]
```

## Arguments

| Arg | Description |
|-----|-------------|
| description | Short task description (3-5 words) |
| prompt | Detailed prompt for the agent |
| agent | Agent type (explore, librarian, etc.) |
| parent_session | Parent session ID |
| autonomy_level | low, medium (default), or high |

## Examples

```bash
# Launch with medium autonomy (default)
python hooks/background-manager.py launch "Find Python files" "Find all .py files in current directory" explore "main"

# Launch with low autonomy (read-only)
python hooks/background-manager.py launch "Safe analysis" "Analyze the codebase structure" explore "main" low

# Launch with high autonomy (can modify files)
python hooks/background-manager.py launch "Implement feature" "Add authentication to the API" explore "main" high
```

## Checking Results

```bash
# List all tasks
python hooks/background-manager.py list

# Check specific task output
python hooks/background-manager.py output <task_id>
```

## Parallel Execution

Launch multiple tasks in sequence - they will all run in parallel:

```bash
python hooks/background-manager.py launch "Find Python" "Find all .py files" explore "main"
python hooks/background-manager.py launch "Find JSON" "Find all .json files" explore "main"
python hooks/background-manager.py launch "Find MD" "Find all .md files" explore "main"
```

All tasks run simultaneously in background.
