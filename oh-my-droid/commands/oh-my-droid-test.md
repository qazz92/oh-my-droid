---
description: Generate comprehensive tests with the test-engineer droid - unit, integration, edge cases
argument-hint: <file, function, or "coverage">
---

Delegate this to the **test-engineer** droid via the Task tool.

Test target: $ARGUMENTS

The test-engineer must:
1. **Discover**: Find existing test files, understand test framework and patterns used in the project
2. **Analyze**: Read code under test, identify testable behaviors and edge cases
3. **Plan**: List test cases covering happy path, edge cases, error conditions, boundary values
4. **Write**: Create tests following existing project conventions (same framework, same patterns)
5. **Run**: Execute tests and fix any failures
6. **Report**: Coverage of behaviors tested and what remains uncovered

Test behavior, not implementation details. Use the project's existing test framework.

Output: Test File, Coverage (happy path, edges, errors), Test Results, Not Covered.
