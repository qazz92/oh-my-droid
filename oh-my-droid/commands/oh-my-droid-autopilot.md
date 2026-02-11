---
description: Auto-route and execute task with intelligent droid selection
---

# Autopilot Command

Automatically analyzes tasks and routes to the best droid.

## Usage

```bash
/oh-my-droid-autopilot <task description>
```

## How it works

1. **Analyze**: AI analyzes task complexity and type
2. **Route**: Selects optimal droid based on task
3. **Execute**: Routes to selected droid with autonomy level

## Droid Selection

| Droid | Best For | Autonomy |
|-------|-----------|----------|
| basic-searcher | Simple searches | Low |
| basic-reader | Code explanation | Low |
| executor-med | Implementation | Medium |
| executor-high | Complex implementation | High |
| hephaestus | Complex architecture | High |
| code-reviewer | Reviews | Medium |
| verifier | Validation | Medium |

## Examples

```bash
# Simple search - routes to basic-searcher
/oh-my-droid-autopilot "find all TODO comments"

# Implementation - routes to executor-med
/oh-my-droid-autopilot "fix the authentication bug"

# Complex - routes to hephaestus
/oh-my-droid-autopilot "design a microservices architecture"
```

## Integration

Uses `intelligent-router.py` for droid selection and `state-manager.py` for tracking.
