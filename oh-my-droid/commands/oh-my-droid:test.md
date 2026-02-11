---
description: Generate tests or analyze coverage with the test-engineer droid
argument-hint: <file, function, or "coverage">
---

Delegate this to the **test-engineer** droid.

Test target: $ARGUMENTS

The test-engineer should:
1. Identify functions and modules needing tests
2. Generate unit tests using AAA pattern (Arrange, Act, Assert)
3. Create integration tests where appropriate
4. Add edge case coverage
5. Run coverage analysis and report gaps
6. Suggest additional tests for uncovered paths
