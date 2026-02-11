---
description: Systematic code refactoring with safety guarantees
argument-hint: <target>
---

Refactor `$ARGUMENTS` with safety:

1. Analyze current code structure
2. Identify refactoring opportunities
3. Apply safe transformations
4. Verify tests still pass

Patterns:
- extract-method, rename-variable
- simplify-condition, remove-dead-code
- async-await conversion

Safety levels: strict (suggestions only), moderate (safe), lax (all)
