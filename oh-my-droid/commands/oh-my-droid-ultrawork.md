---
description: Maximum parallel task execution - decomposes and runs subtasks simultaneously
argument-hint: <task description>
---

You MUST invoke the **ultrawork** skill using the Skill tool:

Skill: ultrawork

User task: $ARGUMENTS

Ultrawork maximizes parallelism:
1. Decompose the task into independent subtasks
2. Launch all subtasks in parallel using the Task tool
3. Monitor progress of each subtask
4. Aggregate results into a final report

Use parallel droid execution for independent subtasks. Do NOT run them sequentially.
