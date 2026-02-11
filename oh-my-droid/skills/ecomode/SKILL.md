---
name: ecomode
description: Token-efficient execution modifier. Optimizes droid routing to prefer simpler, cheaper tiers while maintaining quality.
---

<Purpose>
Ecomode is a MODIFIER, not a standalone execution mode. It overrides default droid selection to prefer simpler tiers, reducing token usage while maintaining quality for tasks that don't require maximum capability.
</Purpose>

<Use_When>
- User says "eco", "ecomode", "efficient", "save tokens", "budget mode"
- Tasks are straightforward and don't need complex reasoning
- Running multiple small tasks where token costs add up
- Combining with other modes: "eco ralph", "eco ultrawork", "eco autopilot"
</Use_When>

<Do_Not_Use_When>
- Task genuinely requires deep reasoning or complex analysis
- Security-sensitive changes that need thorough review
- Architecture decisions that affect the entire system
</Do_Not_Use_When>

<Why_This_Exists>
Not every task needs the most capable droid. Simple changes, searches, and documentation can be handled by lighter droids. Ecomode systematically downtiers droid selection to save tokens without sacrificing correctness for appropriate tasks.
</Why_This_Exists>

<Routing_Rules>
| Default Tier | Ecomode Override |
|-------------|-----------------|
| executor-high / hephaestus | executor-med first, escalate only if needed |
| executor-med | executor-low first, executor-med if fails |
| executor-low | executor-low (no change) |

**ALWAYS prefer lower tiers. Only escalate when task genuinely requires it.**
</Routing_Rules>

<Combining_With_Other_Modes>
| Combination | Effect |
|------------|--------|
| `eco ralph` | Ralph loop with cheaper droids |
| `eco ultrawork` | Parallel execution with cheaper droids |
| `eco autopilot` | Full autonomous with cost optimization |
</Combining_With_Other_Modes>

<Droid_Selection_In_Ecomode>
**Preference order:**
```
PREFERRED - Use for most tasks:
  executor-low, basic-searcher, basic-reader

FALLBACK - Only if LOW fails:
  executor-med, explore

AVOID - Only for planning/critique if essential:
  executor-high, hephaestus, prometheus
```
</Droid_Selection_In_Ecomode>

<Token_Savings_Tips>
1. Batch similar tasks to one droid instead of spawning many
2. Use basic-searcher for file discovery, not explorer
3. Prefer executor-low for simple changes -- only upgrade if it fails
4. Use docs-writer for documentation tasks
5. Avoid hephaestus unless task genuinely requires architecture-level reasoning
</Token_Savings_Tips>

<Steps>
1. Analyze the task complexity honestly
2. Start with the lowest viable droid tier
3. If the droid fails or task clearly needs more capability, escalate ONE tier
4. Apply lightweight verification (build + affected tests only)
</Steps>

<Final_Checklist>
- [ ] Used the lowest viable droid tier
- [ ] Only escalated when clearly needed
- [ ] Build passes
- [ ] Affected tests pass
</Final_Checklist>
