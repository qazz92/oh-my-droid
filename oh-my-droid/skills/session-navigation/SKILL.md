---
name: session-navigation
description: Session management and navigation between tasks
---

# Session Navigation Skill

Navigate and manage sessions efficiently.

## When to Use

- Switching between tasks
- Session state management
- Context switching
- Multi-project workflows

## What This Skill Does

### Session Management

```typescript
listSessions()
switchSession(sessionId)
createSession(name, context)
exportSession(sessionId)
```

### Context Preservation

- Save current task state
- Preserve file changes
- Remember tool outputs
- Restore on switch

## Best Practices

1. Name sessions descriptively
2. Commit before switching
3. Use context labels
