---
description: Fast codebase search - find files, patterns, symbols, and dependencies
argument-hint: <pattern, symbol, or search query>
---

Delegate this to the **explore** droid via the Task tool.

Search for: $ARGUMENTS

The explore droid must:
1. Use Glob for file structure discovery, Grep for content patterns
2. Read key files only when context is needed around matches
3. Return results with file:line references
4. If deeper analysis is needed, recommend the appropriate droid (oracle for debugging, metis for requirements)

Output: Files Found, Pattern Matches, Structure overview (if relevant).
