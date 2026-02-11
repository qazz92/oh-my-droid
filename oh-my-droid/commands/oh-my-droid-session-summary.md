---
description: Generate comprehensive summary of the current development session
argument-hint: --brief --export
---

Generate a session summary covering:

1. **Duration**: Session time and files modified count
2. **Work Completed**: Tasks finished with outcomes
3. **Key Decisions**: Architectural choices and rationale
4. **Code Changes**: Files created, modified, deleted with brief descriptions
5. **Pending Items**: Unfinished tasks and follow-up actions
6. **Verification Status**: Tests passing, build status, known issues

Review the TODO list, git diff, and recent tool usage to compile the summary.

Options:
- `--brief`: Compact 5-line summary
- `--export json`: Machine-readable format
- `--export markdown`: Full markdown report
