---
name: code-cleanup
description: Automated code cleanup for linting, formatting, and dead code removal
user-invocable: true
---

# Code Cleanup Skill

Automated code cleanup and maintenance for improved code quality.

## When to Use
- Before committing code
- During code review feedback
- When technical debt accumulates

## What_You_MUST_Do>
1. RUN linter with auto-fix
2. RUN formatter
3. REMOVE unused imports and variables
4. VERIFY build still passes
5. VERIFY tests still pass

## What_You_MUST_NOT_Do>
1. DO NOT change logic during cleanup
2. DO NOT add new features
3. DO NOT refactor functionality
4. DO NOT skip verification after cleanup

## What This Skill Does

### 1. Linting Fixes
```typescript
// Before
const x=     1;

// After
const x = 1;
```

### 2. Import Organization
```typescript
import { a } from './a';
import { b } from './b';
import { z } from 'external';
```

### 3. Type Annotations
```typescript
function add(a: number, b: number): number {
  return a + b;
}
```

### 4. Dead Code Removal
- Unused imports
- Unused variables
- Unreachable statements

## Usage
`/code-cleanup` to invoke this skill.
