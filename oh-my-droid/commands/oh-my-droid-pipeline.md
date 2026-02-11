---
description: Sequential multi-stage execution - each stage outputs to the next
argument-hint: <task description>
---

You MUST invoke the **pipeline** skill using the Skill tool:

Skill: oh-my-droid:pipeline

User task: $ARGUMENTS

Pipeline executes tasks in sequential stages:
1. Stage 1 (Plan): prometheus droid creates implementation plan
2. Stage 2 (Implement): executor-med droid implements based on plan
3. Stage 3 (Verify): verifier droid runs tests and validates
4. Stage 4 (Package): executor-med droid finalizes

Each stage passes its output to the next. Do NOT skip stages.
