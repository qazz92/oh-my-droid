---
name: pipeline
description: Sequential multi-stage execution where each stage's output feeds the next. Chain droids together in defined workflows.
---

<Purpose>
Pipeline chains multiple droids together in sequential or branching workflows where the output of one droid becomes the input to the next. It creates powerful droid pipelines for structured, multi-phase tasks.
</Purpose>

<Use_When>
- Task has clear sequential phases where each depends on the previous
- User says "pipeline", "stage", "chain", or describes a multi-phase workflow
- Work benefits from structured handoff between specialist droids
- Need to combine research, planning, implementation, and review in order
</Use_When>

<Do_Not_Use_When>
- All tasks are independent -- use `ultrawork` for parallel execution
- Task needs persistence and retry -- use `ralph`
- Task is a single-step operation -- delegate directly to a droid
</Do_Not_Use_When>

<Why_This_Exists>
Complex tasks benefit from structured phases where specialist droids handle what they're best at. A researcher gathers context, a planner designs the approach, an executor implements, and a verifier checks. Pipeline ensures clean handoff between phases with full context passing.
</Why_This_Exists>

<Pipeline_Presets>

### Review Pipeline
```
/oh-my-droid-pipeline review <task>
```
**Stages:**
1. `explore` - Find relevant code and patterns
2. `prometheus` - Analyze and plan approach
3. `momus` - Critique the plan
4. `executor-med` - Implement with full context

**Use for:** Major features, refactorings, complex changes

### Implement Pipeline
```
/oh-my-droid-pipeline implement <task>
```
**Stages:**
1. `prometheus` - Create implementation plan
2. `executor-med` - Implement the plan
3. `test-engineer` - Add/verify tests
4. `verifier` - Verify completion

**Use for:** New features with clear requirements

### Debug Pipeline
```
/oh-my-droid-pipeline debug <issue>
```
**Stages:**
1. `explore` - Locate error locations and related code
2. `oracle` - Analyze root cause
3. `executor-med` - Apply fixes
4. `verifier` - Verify fix works

**Use for:** Bugs, build errors, test failures

### Research Pipeline
```
/oh-my-droid-pipeline research <topic>
```
**Stages:**
1. `librarian` - External docs and API research
2. `explorer` - Internal codebase analysis
3. `prometheus` - Synthesize findings into recommendations

**Use for:** Technology evaluation, architecture decisions

### Security Pipeline
```
/oh-my-droid-pipeline security <scope>
```
**Stages:**
1. `security-auditor` - Vulnerability scan
2. `code-reviewer` - Code quality review
3. `executor-med` - Fix critical issues
4. `verifier` - Verify fixes

**Use for:** Security hardening, pre-release audits
</Pipeline_Presets>

<Custom_Pipelines>
Users can define custom pipelines by specifying stages:
```
/oh-my-droid-pipeline custom "Stage1: explore, Stage2: executor-med, Stage3: verifier" <task>
```

### Branching Pipelines
Route to different droids based on output:
```
explore -> {
  if "complex refactoring" -> prometheus -> executor-high
  if "simple change" -> executor-low
  if "needs research" -> librarian -> executor-med
}
```

### Parallel-Then-Merge
Run droids in parallel, merge outputs:
```
parallel(explore, librarian) -> prometheus -> executor-med
```
</Custom_Pipelines>

<Steps>
1. **Select preset** or parse custom pipeline definition
2. **Execute Stage 1**: Spawn first droid, collect output
3. **Pass context**: Feed Stage 1 output as context to Stage 2
4. **Repeat**: Continue through all stages with context accumulation
5. **Report**: Final summary with results from each stage
</Steps>

<Output_Format>
## Pipeline Results

### Stage 1: [Droid] - [Status]
[Summary of output]

### Stage 2: [Droid] - [Status]
[Summary of output]

### Final Result
[Aggregated outcome]
</Output_Format>

<Failure_Modes_To_Avoid>
- Lost context: Not passing previous stage output to next stage. Always include full context.
- Wrong preset: Using "debug" pipeline for a new feature. Match preset to task type.
- Skipping stages: Jumping from research to implementation without planning.
- No verification: Pipeline ends at implementation without a verification stage.
</Failure_Modes_To_Avoid>
