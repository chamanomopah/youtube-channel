---
description: Orchestrate specialized agents. Creates agent teams with coordinated task execution.
argument-hint: [objective] [--workflow WORKFLOW_NAME] [orchestration-guidance]
disallowed-tools: Task, EnterPlanMode
model: opus
---

# Orchestrate Agents

Create and coordinate teams of specialized agents using TaskCreate, TaskUpdate, and Task delegation.

## Arguments

- `$1`: **OBJECTIVE** (required) - Main objective or problem to solve
- `--workflow WORKFLOW_NAME` (optional) - Predefined workflow from `.claude/commands/workflows/`
- Remaining args: **ORCHESTRATION_GUIDANCE** - Optional guidance for agent specialization

## Workflow Mode

**With `--workflow` flag:**
1. Load `.claude/commands/workflows/[WorkflowName].md`
2. Execute command sequence exactly
3. Follow workflow's parallel/sequential strategy

**Without `--workflow`:** Proceed with custom orchestration (Phases 1-8 below).

## Available Workflows

| Workflow | Purpose | Use Case |
|----------|---------|----------|
| **SimpleSdlc** | plan → implement → test → review | Simple features, bug fixes |
| **TeamSdlc** | Parallel team orchestration | Complex, full-stack work |
| **QuickPatch** | Rapid bug fix | Hotfixes, quick corrections |

## CRITICAL: Orchestrator Role

```markdown
🚫 NEVER:
- Read files yourself (delegate to Explore)
- Write code yourself (delegate to Builder)
- Run commands yourself (delegate to agents)
- Use Skill tool (executes in YOUR context!)

✅ ALWAYS:
- Create task list with TaskCreate FIRST
- Delegate via Task tool with specialized subagent_type
- Monitor with TaskOutput and TaskList
- Update status with TaskUpdate
- Aggregate summaries (NOT full context)
```

**Why?** Follows @docs/tac/multi-agent-context-protection.md - keeps context lean, enables parallelization.

## Instructions

### Mode Selection

**If `--workflow` specified:**
1. Read workflow file (ONLY file you read)
2. Parse command sequence and dependencies
3. Create task structure with TaskCreate
4. Set dependencies with TaskUpdate
5. **DELEGATE each step via Task tool** (not Skill tool):
   ```javascript
   Task({
     description: "<Step name>",
     prompt: `Read .claude/commands/<command>.md and execute with objective: "<objective>"
              Report: 1) What done, 2) Files changed, 3) Next steps`,
     subagent_type: "<appropriate agent>",
     model: "sonnet", // or "opus" for complex
     run_in_background: <true for parallel, false for sequential>
   })
   ```
6. Monitor with TaskOutput
7. Aggregate results (summaries only!)

**If no workflow:** Proceed with custom orchestration.

### Custom Mode Phases

#### Phase 1: Analyze Requirements
- Parse OBJECTIVE from `$1` (ask user if missing)
- Identify complexity (simple|medium|complex)
- Determine agent types and command allocation

#### Phase 2: Design Agent Team
For each agent, define:
```
Name: <unique>
Role: <specialization>
Type: <subagent_type>
Commands: <specific commands to use>
```

**Patterns:**
- Builder: Write/Edit/Bash
- Explorer: Grep/Glob/Read
- Validator: Tests/verification
- Specialist: Domain-specific

#### Phase 3: Create Task Structure
**BEFORE deploying agents:**
```javascript
TaskCreate({
  subject: "Research auth patterns",
  description: "Find current auth implementation",
  activeForm: "Researching auth patterns"
}) // Returns taskId
```

#### Phase 4: Set Dependencies
```javascript
TaskUpdate({
  taskId: "2",
  addBlockedBy: ["1"] // Task 2 waits for Task 1
})
```

**Patterns:**
- Sequential: A → B → C
- Parallel: A + B → C
- Diamond: A → B/D → C

#### Phase 5: Deploy Agents
```javascript
Task({
  description: "Research auth",
  prompt: "Use Grep/Glob/Read to find auth code. Report findings with file refs.",
  subagent_type: "Explore",
  model: "sonnet",
  run_in_background: false // Sequential
})

// Parallel execution
Task({
  description: "Implement login",
  prompt: "Create POST /auth/login endpoint per design doc",
  subagent_type: "general-purpose",
  model: "sonnet",
  run_in_background: true // Parallel
})
```

#### Phase 6: Monitor Progress
```javascript
// Check all tasks
TaskList({})

// Get specific task
TaskGet({ taskId: "1" })

// Update status
TaskUpdate({
  taskId: "1",
  status: "in_progress",
  owner: "agent-1"
})

// Check agent output (for background tasks)
TaskOutput({
  task_id: "agent-3",
  block: true, // Wait for completion
  timeout: 300000
})
```

#### Phase 7: Resume or Fresh
```javascript
// Resume: Related work, needs prior context
Task({
  prompt: "Now add refresh token endpoint",
  resume: "agent-2" // Same agent, preserved context
})

// Fresh: New task, clean slate
Task({
  description: "Write tests",
  subagent_type: "general-purpose" // New agent
})
```

#### Phase 8: Validation
```javascript
TaskCreate({
  subject: "Validate system",
  description: "Run tests, verify acceptance criteria",
  activeForm: "Validating system"
})

Task({
  description: "Validate",
  prompt: "Run validation commands. Verify: 1) Tests pass, 2) Criteria met",
  subagent_type: "validator"
})
```

## How to Delegate (CRITICAL)

### ❌ WRONG: Skill Tool
```javascript
Skill({ skill: "plan" })
// Executes in YOUR context! Violates Meta-Prompt HOP pattern!
```

### ✅ CORRECT: Task Tool
```javascript
Task({
  description: "Create plan",
  prompt: `Read .claude/commands/plan.md and execute with: "<objective>"
           Report: 1) Plan location, 2) Summary`,
  subagent_type: "Plan",
  model: "opus"
})
// Fresh agent, clean context!
```

## Key Principles

1. **ORCHESTRATE, DON'T EXECUTE** - Always delegate
2. **Plan first** - Create task list before deploying
3. **Clear dependencies** - Use addBlockedBy explicitly
4. **Track ownership** - Update owner field
5. **Monitor progress** - Check TaskList regularly
6. **Resume wisely** - Related = resume, unrelated = fresh
7. **Validate last** - Always include validation task
8. **Keep context lean** - You're orchestrator, not specialist

## Anti-Patterns

| Pattern | Wrong | Correct |
|---------|-------|---------|
| Reading files | "Let me read..." | Delegate to Explore |
| Commands | "I'll run /plan" | Delegate via Task |
| Writing code | "I'll create..." | Delegate to Builder |
| No tasks | Launching without TaskCreate | Always create tasks first |
| Full context | Copying file contents | Pass summaries only |

## Example: SimpleSdlc

```bash
/orchestrate-agents "Add login page" --workflow SimpleSdlc
```

**Execution:**
1. Create tasks for plan, implement, test, review
2. Set sequential dependencies
3. Delegate each step via Task tool:
   - Plan agent reads plan.md, creates plan
   - Builder agent reads implement.md, uses plan
   - Tester agent runs tests
   - Reviewer agent validates against spec

## Report Format

```markdown
## Orchestration Complete

**Objective:** <summary>

### Agents Deployed
- <Agent> (<Type>): <role> - <status>

### Task Summary
✅ Task 1: <subject> - completed
✅ Task 2: <subject> - completed

### Files Created/Modified
- <file1> - <purpose>

### Next Steps
<verification or remaining work>
```

## Creating Workflows

```bash
/create-workflow [WorkflowName] "[description]"
```

Creates workflow file with command sequence, agent requirements, parallel/parallel strategy.

## Notes

- See @memory/orchestration-patterns.md for detailed patterns
- See @docs/tac/multi-agent-context-protection.md for principles
- See @docs/tac/one-agent-one-purpose.md for specialization
- Document agent session IDs for resume capability
- Test with simple objectives first
