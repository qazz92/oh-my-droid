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

## What_You_MUST_Do>
1. SCAN for hardcoded secrets (API keys, passwords, tokens)
2. CHECK dependencies for known CVEs
3. IDENTIFY insecure coding patterns
4. REPORT findings with severity and remediation
5. PROVIDE secure code examples

## What_You_MUST_NOT_Do>
1. DO NOT skip dependency scanning
2. DO NOT report without remediation suggestions
3. DO NOT ignore low-severity issues in security-sensitive code
4. DO NOT commit secrets to version control

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
