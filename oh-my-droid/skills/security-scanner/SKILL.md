---
name: security-scanner
description: Security scanning for secrets and vulnerabilities
user-invocable: true
---

# Security Scanner Skill

Security scanning and vulnerability detection.

## When to Use

- Pre-commit security checks
- Code review analysis
- Dependency scanning

## What This Skill Does

### Secret Detection

```typescript
// BAD
const API_KEY = "sk-1234567890abcdef";

// GOOD
const API_KEY = process.env.API_KEY;
```

### Vulnerability Scanning

- Known CVEs in dependencies
- Insecure coding patterns
- SQL injection risks
- XSS vulnerabilities

## Usage

`/security-scan` to run a security scan.
