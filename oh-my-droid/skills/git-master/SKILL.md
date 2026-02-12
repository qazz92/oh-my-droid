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

## What_You_MUST_Do>
1. CHECK git status BEFORE any operation
2. REVIEW changes with git diff BEFORE committing
3. CREATE atomic commits (one logical change per commit)
4. WRITE clear commit messages following project style
5. VERIFY commit succeeded with git status

## What_You_MUST_NOT_Do>
1. DO NOT commit without reviewing changes
2. DO NOT mix unrelated changes in one commit
3. DO NOT push without explicit user request
4. DO NOT use -i flag (interactive mode not supported)
5. DO NOT commit secrets or sensitive data

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
