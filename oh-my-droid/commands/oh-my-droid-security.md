---
description: Run a security audit on files or modules with the security-auditor droid
argument-hint: <files, directory, or module>
---

Delegate this to the **security-auditor** droid.

Audit target: $ARGUMENTS

The security-auditor should:
1. Scan for injection vulnerabilities (SQL, command, XSS)
2. Check for insecure transport and privilege escalation
3. Detect secrets exposure and hardcoded credentials
4. Suggest concrete mitigations with CWE references
5. Report findings by file with severity levels
