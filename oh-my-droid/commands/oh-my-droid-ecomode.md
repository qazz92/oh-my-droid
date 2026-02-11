---
description: Token-efficient execution - minimize tool calls and context for budget-conscious tasks
argument-hint: <task description>
---

You MUST invoke the **ecomode** skill using the Skill tool:

Skill: ecomode

User task: $ARGUMENTS

Ecomode optimizes for token efficiency:
1. Minimize tool calls - batch operations when possible
2. Use precise Grep patterns instead of broad searches
3. Check cached state before re-reading files
4. Only include relevant code snippets in context
5. Prefer direct edits with exact targets

Be concise in all responses. Avoid redundant operations.
