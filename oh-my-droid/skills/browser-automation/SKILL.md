---
name: browser-automation
description: Web browser automation for testing and data extraction
---

# Browser Automation Skill

Automated web browser interactions.

## When to Use

- Form filling and submission
- Screenshot capture
- Data extraction
- E2E testing

## Capabilities

### Navigation
```typescript
await navigate("https://example.com")
await goBack()
await refresh()
```

### Interaction
```typescript
await click(selector)
await type(selector, "text")
await select(selector, "option")
```

### Verification
```typescript
await expect(selector).toBeVisible()
await takeScreenshot("page.png")
```

## Usage

Use with CDP (Chrome DevTools Protocol) tools.
