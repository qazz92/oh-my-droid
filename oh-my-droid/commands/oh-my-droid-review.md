---
description: Validate and critique a plan for gaps, risks, and feasibility before execution
argument-hint: <plan file, task description, or implementation details>
---

Delegate this to the **momus** droid via the Task tool.

Review target: $ARGUMENTS

Momus must:
1. **Read the plan** and understand goals, phases, and tasks
2. **Validate against codebase**: Do referenced files exist? Are assumptions correct?
3. **Gap analysis**: Missing error handling? Edge cases? Tests? Rollback strategy?
4. **Risk assessment**: What could go wrong? Are estimates realistic?
5. **Dependency check**: Are task dependencies correctly ordered?

Rate each issue: CRITICAL (blocks execution), HIGH (will cause rework), MEDIUM (should address), LOW (nice to have).
Every criticism must include a suggestion for improvement.

Verdict: APPROVE / REVISE (with specific changes) / REJECT (with reasons).
