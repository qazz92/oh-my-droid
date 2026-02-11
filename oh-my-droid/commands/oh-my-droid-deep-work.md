---
description: Complex autonomous implementation with the hephaestus droid - architecture, system design, multi-module changes
argument-hint: <feature or task description>
---

Delegate this to the **hephaestus** droid via the Task tool.

Task: $ARGUMENTS

Hephaestus handles architecture-level complexity:
1. **Survey**: Deep exploration of affected modules, interfaces, dependencies
2. **Design**: Architectural approach with rationale and trade-offs
3. **Plan**: TodoWrite with ordered steps respecting dependencies
4. **Implement**: One module at a time, maintaining system consistency
5. **Integrate**: Verify all modules work together after changes
6. **Verify**: Full build + full test suite
7. **Document**: Architecture decisions for future maintainers

Output: Design Decision, Changes Made (file:line), Integration Points, Verification Results, Architecture Notes.
