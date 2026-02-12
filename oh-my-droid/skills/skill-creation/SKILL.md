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

## What_You_MUST_Do>
1. USE kebab-case naming (e.g., `code-cleanup`)
2. WRITE clear, single-purpose description
3. INCLUDE When to Use section
4. INCLUDE What_You_MUST_Do and What_You_MUST_NOT_Do sections
5. PROVIDE examples

## What_You_MUST_NOT_Do>
1. DO NOT create multi-purpose skills
2. DO NOT use vague descriptions
3. DO NOT skip MUST/MUST_NOT sections
4. DO NOT use camelCase or snake_case naming

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

## What_You_MUST_Do>

## What_You_MUST_NOT_Do>

## What This Skill Does

## Examples
```

## Naming Conventions
- kebab-case: `code-cleanup`
- Descriptive purpose
- Single responsibility
