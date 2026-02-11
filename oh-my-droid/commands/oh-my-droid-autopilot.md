---
description: Full autonomous execution from idea to working code - plan, execute, QA, validate
argument-hint: <task description>
---

You MUST invoke the **autopilot** skill using the Skill tool to handle this task fully autonomously.

Skill: autopilot

User task: $ARGUMENTS

## Execution Policy

Autopilot runs the full lifecycle without user intervention:

1. **Phase 0 - Expansion**: Turn the user's idea into a detailed spec
   - Spawn **prometheus** droid to extract requirements and create technical spec
   - Save spec to `.omd/autopilot/spec.md`

2. **Phase 1 - Planning**: Create implementation plan from spec
   - Spawn **prometheus** droid for plan creation
   - Spawn **momus** droid to validate the plan
   - Save plan to `.omd/plans/autopilot-impl.md`

3. **Phase 2 - Execution**: Implement using appropriate droids
   - **executor-low**: Simple, low-risk tasks
   - **executor-med**: Standard implementation tasks (default)
   - **executor-high**: Complex implementation requiring broad tool access
   - **hephaestus**: Architecture-level, system design tasks
   - Run independent tasks in parallel via Task tool

4. **Phase 3 - QA**: Cycle until all checks pass
   - Build, lint, typecheck, test
   - Fix failures and retry (max 5 cycles)
   - Stop early if the same error repeats 3 times (fundamental issue)

5. **Phase 4 - Validation**: Multi-perspective review
   - **code-reviewer**: Code quality and patterns
   - **security-auditor**: Vulnerability check
   - **verifier**: Functional correctness
   - All must approve; fix and re-validate on rejection

6. **Phase 5 - Cleanup**: Remove state files on success
   - Delete `.omd/state/autopilot-state.json` and related state files

## Rules

- Each phase must complete before the next begins
- Use parallel execution within phases where possible (Phase 2, Phase 4)
- QA cycles repeat up to 5 times; same error 3 times = stop and report
- Do NOT stop until all phases are complete or a fundamental blocker is found
- If requirements are too vague, pause and ask the user before proceeding
