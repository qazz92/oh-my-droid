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

## What_You_MUST_Do>
1. DISCOVER existing test patterns FIRST
2. USE existing test framework (do NOT introduce new ones)
3. COVER happy path, edge cases, AND error conditions
4. RUN tests after writing to verify they pass
5. REPORT coverage of behaviors tested

## What_You_MUST_NOT_Do>
1. DO NOT test only happy path
2. DO NOT test implementation details - test behavior
3. DO NOT introduce new test frameworks
4. DO NOT write tests without running them
5. DO NOT modify production code logic

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
