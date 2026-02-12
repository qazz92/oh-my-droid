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

## What_You_MUST_Do>
1. NAME sessions descriptively
2. COMMIT before switching sessions
3. SAVE current task state
4. USE context labels for organization
5. RESTORE context on switch

## What_You_MUST_NOT_Do>
1. DO NOT switch without saving state
2. DO NOT use vague session names
3. DO NOT forget to preserve file changes
4. DO NOT lose tool outputs when switching

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
