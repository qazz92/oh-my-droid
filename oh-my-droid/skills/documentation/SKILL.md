---
name: documentation
description: Automated documentation generation and maintenance
user-invocable: true
---

# Documentation Skill

Generate and maintain documentation.

## When to Use

- Documenting new functions
- Updating outdated docs
- Creating API documentation

## What This Skill Does

### JSDoc Generation

```typescript
/**
 * Calculates the total price of all items.
 *
 * @param items - Array of cart items
 * @returns The sum of all item prices
 */
function calculateTotal(items: CartItem[]): number { }
```

### README Generation

- Installation instructions
- Usage examples
- API reference

## Usage

`/docs-generate <file>` to create documentation.
