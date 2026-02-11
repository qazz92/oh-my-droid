---
description: Execute approved plan by delegating subtasks to specialist droids with parallel coordination
argument-hint: <approved plan or task breakdown>
---

Delegate this to the **orchestrator** droid via the Task tool.

Execute plan: $ARGUMENTS

The orchestrator must:
1. **Analyze**: Parse the plan into subtasks, identify dependencies and parallelism
2. **Select droids**: Match each subtask to the right specialist droid
3. **Execute**: Fire independent tasks simultaneously via Task tool, run dependent tasks sequentially
4. **Monitor**: Check results from each droid, handle failures
5. **Aggregate**: Combine results into a coherent final report
6. **Verify**: Ensure all subtasks completed and results are consistent

Droid selection:
- Simple changes: executor-low
- Standard work: executor-med (default)
- Complex work: executor-high / hephaestus
- Research: explore / librarian
- Testing: test-engineer / verifier
- Review: code-reviewer / security-auditor

Fire independent subtasks in parallel. Do NOT serialize independent work.
