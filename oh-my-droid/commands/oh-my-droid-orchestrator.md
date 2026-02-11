---
description: Orchestrate task execution based on approved plan and review
argument-hint: <approved plan and task>
---

# Orchestrator Command

Execute tasks based on approved plan and completed review.

## Workflow

```
1. /oh-my-droid-plan       # User creates plan
2. /oh-my-droid-review    # User reviews plan
3. /oh-my-droid-orchestrator  # Execute based on approved plan
```

## Usage

```bash
/oh-my-droid-orchestrator "<approved plan>"
```

## What to Provide

- Approved plan from `/oh-my-droid-plan`
- Review confirmation from `/oh-my-droid-review`
- Task breakdown and subtasks

## Execution Steps

1. Parse approved plan
2. Allocate droids to subtasks
3. Execute subtasks sequentially or in parallel
4. Monitor progress
5. Report completion status

## Droid Allocation

| Subtask Type | Droid |
|-------------|-------|
| Implementation | executor-med, executor-high |
| Search/Research | explorer, librarian |
| Testing | test-engineer, verifier |
| Documentation | docs-writer |
| Security | security-auditor |

## Example

```
User: "/oh-my-droid-orchestrator Based on approved plan:
- Subtask 1: Create API endpoints (executor-med)
- Subtask 2: Add authentication (executor-high)
- Subtask 3: Write unit tests (test-engineer)
- Subtask 4: Verify tests pass (verifier)"
```

Then orchestrator executes each subtask with appropriate droids.
