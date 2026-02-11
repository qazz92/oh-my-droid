---
description: Systematic code refactoring with safety guarantees - executor-med handles implementation
argument-hint: <target file, function, or module>
---

Delegate this to the **executor-med** droid via the Task tool.

Refactor target: $ARGUMENTS

The executor-med must follow a safe refactoring workflow:
1. **Analyze**: Read current code, identify refactoring opportunities
2. **Plan**: List specific transformations (extract method, rename, simplify condition, remove dead code)
3. **Verify baseline**: Run tests BEFORE refactoring to establish green baseline
4. **Apply**: Make transformations one at a time, smallest viable diff
5. **Verify each step**: Run tests after each transformation to catch regressions
6. **Report**: List all changes with file:line references and verification results

Safety rules:
- Tests must pass before AND after each transformation
- No behavior changes unless explicitly requested
- If tests fail after a transformation, revert and report
