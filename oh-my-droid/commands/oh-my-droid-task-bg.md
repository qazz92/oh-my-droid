---
description: Launch background tasks for parallel execution with any droid
argument-hint: <description> <prompt>
---

# Task-bg

Launch background tasks that run in parallel using any available droid.

## Usage

```
/task-bg <description> <prompt>
```

## Arguments

- `description`: Short task description (3-5 words)
- `prompt`: Detailed prompt for the droid

## Examples

```markdown
# Launch background tasks (defaults to --auto medium)
/task-bg "Find Python files" "Find all .py files in the current directory"
/task-bg "Find auth patterns" "Find all authentication implementations..."
/task-bg "Review security" "Review the auth module for security issues..."
/task-bg "Check tests" "Analyze test coverage..."
```

## How It Works

1. Creates a background task with droid exec
2. Executes in parallel with other /task-bg commands
3. Use "python hooks/background-manager.py list" to check status

## Autonomy Levels

| Level | Permissions | Use Case |
|-------|-------------|----------|
| `low` | Read-only, file creation | Safe analysis, documentation |
| `medium` | Dev ops, git local | Most development tasks |
| `high` | Production ops | Deployments, CI/CD |

To use different autonomy levels, use the Python command directly:

```bash
# low - Safe analysis
python hooks/background-manager.py launch "Safe analysis" "..." explorer "main" low

# medium - Development (default)
python hooks/background-manager.py launch "Dev task" "..." explorer "main" medium

# high - Production operations
python hooks/background-manager.py launch "Deploy" "..." executor-high "main" high
```

## Available Droids

Use these names in your prompts:
- `explorer` - Fast internal code exploration
- `librarian` - External documentation search
- `oracle` - Architecture and debugging
- `code-reviewer` - Code review
- `test-engineer` - Testing
- `security-auditor` - Security analysis
- `executor-med` - Implementation
- `executor-high` - Complex implementation

## Checking Results

```bash
# List running tasks
python hooks/background-manager.py list

# Check specific task
python hooks/background-manager.py status <task_id>
```
