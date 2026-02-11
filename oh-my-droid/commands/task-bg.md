# task-bg

Launch background tasks for parallel execution.

## Usage

```
/task-bg <description> <agent> <prompt>
```

## Arguments

- `description`: Short task description (3-5 words)
- `agent`: Agent type to handle the task
- `prompt`: Full detailed prompt for the agent

## Available Agents

- `explore` - Fast internal code exploration
- `librarian` - External documentation search
- `oracle` - Architecture and debugging
- `code-reviewer` - Code review
- `test-engineer` - Testing
- `security-auditor` - Security analysis

## Examples

```markdown
# Launch a background task
/task-bg "explore auth patterns" explore "Find all authentication implementations in the codebase..."

# Launch multiple tasks in parallel
/task-bg "find JWT docs" librarian "Find current JWT security best practices..."
/task-bg "check test coverage" test-engineer "Analyze current test coverage..."
/task-bg "review security" security-auditor "Review the auth module for vulnerabilities..."
```

## Checking Results

After launching background tasks, check their status:

```bash
# List all background tasks
droid plugin exec hooks/background-manager.py list

# Get status of a specific task
droid plugin exec hooks/background-manager.py status <task_id>
```

## Workflow

1. Launch one or more `/task-bg` commands (they run in parallel)
2. Continue working in the main session
3. Check task results with the commands above
4. Use results in your main workflow
