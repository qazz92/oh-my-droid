---
name: skill-creation
description: Automated skill generation for Droid plugins
---

# Skill Creation Skill

Automated skill generation.

## When to Use

- Creating new skills
- Skill template generation
- Best practice implementation

## What This Skill Does

### Skill Structure

```
skill-name/
├── SKILL.md         # Main skill file
└── (optional assets)
```

### SKILL.md Template

```yaml
---
name: skill-name
description: Brief description
user-invocable: true
---

# Skill Name

## When to Use

## What This Skill Does

## Examples
```

## Naming Conventions

- kebab-case: `code-cleanup`
- Descriptive purpose
- Single responsibility
