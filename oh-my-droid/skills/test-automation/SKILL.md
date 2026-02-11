---
name: test-automation
description: Automated test generation, coverage analysis, and test maintenance
user-invocable: true
---

# Test Automation Skill

Automated test generation and maintenance.

## When to Use

- Adding tests for new features
- Improving test coverage
- Maintaining existing tests

## What This Skill Does

### Test Generation

- Identify functions requiring tests
- Generate happy path tests
- Generate edge case tests
- Generate error handling tests

### Coverage Analysis

```bash
npm test -- --coverage
```

### Mock Generation

```typescript
const mockDatabase = {
  query: vi.fn(),
  connect: vi.fn(),
  disconnect: vi.fn(),
};
```

## Usage

`/test-generate <file>` to generate tests.
