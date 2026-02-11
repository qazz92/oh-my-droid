---
description: Generate or update documentation - API docs, README, architecture guides, inline comments
argument-hint: <target file, module, or "api"|"readme"|"architecture">
---

Delegate this to the **docs-writer** droid via the Task tool.

Documentation target: $ARGUMENTS

The docs-writer must:
1. **Survey**: Read existing docs to understand style, format, and coverage
2. **Analyze**: Read the code being documented to understand actual behavior
3. **Write**: Create documentation following existing project conventions
4. **Verify**: Ensure code examples match actual code and API signatures are correct

Documentation must be grounded in actual code (read it first). Code examples must work. Update existing docs rather than creating duplicates. Keep docs scannable (headings, lists, code blocks).

Output: Files Created/Updated, Coverage of topics documented.
