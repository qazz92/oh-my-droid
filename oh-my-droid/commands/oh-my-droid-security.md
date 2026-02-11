---
description: Security audit with OWASP Top 10 analysis, secrets detection, and dependency audit
argument-hint: <files, directory, or module>
---

Delegate this to the **security-auditor** droid via the Task tool.

Audit target: $ARGUMENTS

The security-auditor must:
1. **Secrets scan**: Grep for hardcoded api keys, passwords, tokens, credentials
2. **Dependency audit**: Run npm audit / pip-audit / cargo audit as appropriate
3. **OWASP Top 10**: Check injection, auth, sensitive data, access control, XSS, security config
4. **Prioritize**: Rate findings by severity x exploitability x blast radius
5. **Remediate**: Provide secure code examples in the SAME language as the vulnerable code

Each finding must include: location (file:line), OWASP category, severity (CRITICAL/HIGH/MEDIUM/LOW), exploitability, blast radius, and remediation with secure code.

Output: Risk Level (HIGH/MEDIUM/LOW), Summary, Issues by severity, Security Checklist.
