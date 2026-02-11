---
description: Systematic code review with severity-rated feedback - spec compliance then code quality
argument-hint: <files, branch, or diff>
---

Delegate this to the **code-reviewer** droid via the Task tool.

Review target: $ARGUMENTS

The code-reviewer must follow two stages:

**Stage 1 - Spec Compliance** (must pass first):
- Does the implementation cover ALL requirements?
- Does it solve the RIGHT problem?
- Anything missing or extra?

**Stage 2 - Code Quality** (only after Stage 1):
- Security: hardcoded secrets, injection, XSS
- Quality: error handling, edge cases, naming
- Performance: unnecessary loops, missing caching
- Best practices: framework conventions, patterns

Every issue must have: file:line reference, severity (CRITICAL/HIGH/MEDIUM/LOW), concrete fix suggestion.

Verdict: APPROVE / REQUEST CHANGES / COMMENT.
