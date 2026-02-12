---
name: ultrawork
description: Parallel execution engine for high-throughput task completion. Runs multiple droids simultaneously for independent tasks.
---

<Purpose>
Ultrawork is a parallel execution engine that runs multiple droids simultaneously for independent tasks. It provides parallelism and smart droid routing but not persistence or verification loops -- those are provided by ralph (which includes ultrawork).
</Purpose>

<Use_When>
- Multiple independent tasks can run simultaneously
- User says "ulw", "ultrawork", or wants parallel execution
- You need to delegate work to multiple droids at once
- Task benefits from concurrent execution
</Use_When>

<Do_Not_Use_When>
- Task requires guaranteed completion with verification -- use `ralph` instead (ralph includes ultrawork)
- Task requires a full autonomous pipeline -- use `autopilot` instead
- There is only one sequential task -- delegate directly to executor-med
- User needs session persistence for resume -- use `ralph`
</Do_Not_Use_When>

<What_You_MUST_Do>
1. CLASSIFY - Identify which tasks are independent vs dependent
2. ROUTE - Select correct droid tier for each task complexity
3. FIRE ALL - Launch ALL independent tasks at once, BEFORE checking ANY
4. WAIT - Only wait for dependent tasks after prerequisites complete
5. VERIFY - Lightweight check: build passes, affected tests pass
</What_You_MUST_Do>

<What_You_MUST_NOT_Do>
1. DO NOT serialize independent tasks - this defeats the purpose
2. DO NOT use wrong tier (hephaestus for typos is wasteful)
3. DO NOT skip verification - at minimum check build and tests
4. DO NOT fire sequentially - fire all, then check all
</What_You_MUST_NOT_Do>

<Why_This_Exists>
Sequential task execution wastes time when tasks are independent. Ultrawork enables firing multiple droids simultaneously, reducing total execution time. It is designed as a composable component that ralph and autopilot layer on top of.
</Why_This_Exists>

<Execution_Policy>
- Fire all independent droid calls simultaneously -- never serialize independent work
- Always select the right droid tier for task complexity
- Run quick commands in foreground, long operations can run via Task tool
</Execution_Policy>

<Parallel_Execution>
Factory Droid does NOT support native background execution (`run_in_background: true`). For TRUE parallel execution of independent tasks, use `background-manager.py`:

```bash
# Launch multiple droids in TRUE parallel (fire ALL before checking ANY)
python3 hooks/background-manager.py launch "Fix auth" "Fix auth module errors" executor-med "main"
python3 hooks/background-manager.py launch "Fix API" "Fix API route errors" executor-med "main"
python3 hooks/background-manager.py launch "Fix UI" "Fix frontend type errors" executor-med "main"

# Monitor all running tasks
python3 hooks/background-manager.py list

# Check specific task output when done
python3 hooks/background-manager.py output <task_id>
```

CRITICAL: Launch ALL independent tasks BEFORE checking any results. Do NOT launch-wait-launch sequentially.
</Parallel_Execution>

<Steps>
1. **Classify tasks by independence**: Identify which can run in parallel vs which have dependencies
2. **Route to correct droids**:
   - Simple changes: executor-low
   - Standard implementation: executor-med (DEFAULT)
   - Complex work: executor-high or hephaestus
3. **Fire independent tasks simultaneously**: Launch all parallel-safe tasks at once via Task tool
4. **Run dependent tasks sequentially**: Wait for prerequisites before launching dependent work
5. **Verify when all tasks complete** (lightweight):
   - Build passes
   - Affected tests pass
   - No new errors introduced
</Steps>

<Examples>
<Good>
Three independent tasks fired simultaneously:
```
Task(subagent_type="executor-low", prompt="Add missing type export for Config interface")
Task(subagent_type="executor-med", prompt="Implement the /api/users endpoint with validation")
Task(subagent_type="executor-med", prompt="Add integration tests for the auth middleware")
```
Why good: Independent tasks at appropriate tiers, all fired at once.
</Good>

<Bad>
Sequential execution of independent work:
```
result1 = Task(executor-low, "Add type export")  # wait...
result2 = Task(executor-med, "Implement endpoint")  # wait...
result3 = Task(executor-med, "Add tests")  # wait...
```
Why bad: Independent tasks serialized, wasting time.
</Bad>

<Bad>
Wrong tier selection:
```
Task(subagent_type="hephaestus", prompt="Add a missing semicolon")
```
Why bad: Overkill for a trivial fix. Use executor-low instead.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- When invoked directly (not via ralph), apply lightweight verification only
- For full persistence and verification, recommend switching to `ralph`
- If a task fails repeatedly, report the issue rather than retrying indefinitely
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All parallel tasks completed
- [ ] Build passes
- [ ] Affected tests pass
- [ ] No new errors introduced
</Final_Checklist>

<Advanced>
## Relationship to Other Modes

```
ralph (persistence wrapper)
 └── includes: ultrawork (this skill)
     └── provides: parallel execution only

autopilot (autonomous execution)
 └── includes: ralph
     └── includes: ultrawork (this skill)

ecomode (modifier)
 └── modifies: ultrawork's droid selection to prefer cheaper tiers
```

Ultrawork is the parallelism layer. Ralph adds persistence and verification. Autopilot adds the full lifecycle pipeline. Ecomode adjusts droid routing.
</Advanced>
