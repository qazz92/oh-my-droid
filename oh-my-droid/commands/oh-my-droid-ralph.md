---
description: Persistent execution with verify/fix loops until task is verified complete (max 3 attempts)
argument-hint: <task description>
---

You MUST invoke the **ralph** skill using the Skill tool:

Skill: ralph

User task: $ARGUMENTS

Ralph ensures task completion through verification and fix loops:
1. Analyze task and route to best droid
2. Execute the task
3. Verify the result
4. If failed, fix and retry (max 3 attempts)
5. Report final result

Do NOT stop until the task is verified complete or max attempts reached.
