---
name: git-master
description: Git expertise for atomic commits, rebasing, and history analysis
user-invocable: true
---

# Git Master Skill

Git expertise for commits, rebasing, and history.

## When to Use

- Creating atomic commits
- Rebase and history cleanup
- Finding when/where changes introduced

## Modes

| Mode | Triggers |
|------|----------|
| COMMIT | "commit" |
| REBASE | "rebase", "squash" |
| HISTORY_SEARCH | "find when", "git blame" |

## Core Principles

### Multiple Commits by Default

```
3+ files → 2+ commits
5+ files → 3+ commits
```

### Style Detection

- **SEMANTIC**: `type: message`
- **PLAIN**: Just description

## Usage

`/git-commit` to create atomic commits.
