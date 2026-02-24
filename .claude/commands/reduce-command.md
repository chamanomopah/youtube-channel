---
description: Reduce command size using R&D framework while maintaining quality and functionality
argument-hint: [command-path]
allowed-tools: Read, Write, Edit
---

# Reduce Command (HOP - Higher-Order Prompt)

**Meta-Prompt Level**: This is a **Level 3 HOP** that accepts another prompt (command) as input and optimizes it.

## Core Pattern

```text
Input Command → Read → Analyze → Reduce → Output Optimized Command
```

Following **@docs/tac/meta-prompt-patterns.md** principles:
- One-shot execution (no conversational back-and-forth)
- Fresh context for analysis
- "think hard" reasoning mode activated

## Framework

Applying **Reduce & Delegate Framework**:
- **Reduce**: Remove verbosity, redundancy, over-detailing
- **Delegate**: Reference @docs, use MCP tools, suggest sub-commands

## Input

Command path: **$1** (default: `c:\.nero\docs\tac\skills\reduce-delegate-framework\SKILL.md`)

## Process

**THINK HARD** about optimization strategy (activates extended reasoning).

### Phase 1: Analyze
1. Read target command
2. Identify: purpose, size (~tokens), reduction opportunities
3. Tag: redundancy, verbosity, duplicate info, static content

### Phase 2: Reduce Strategies

| Technique | Apply When | How |
| --- | --- | --- |
| Condense | Wordy descriptions | Imperative mood, remove fluff |
| Consolidate | Multiple examples | Keep 1-2 representative |
| Reference | Static standard info | Link to @docs:topic/file |
| Simplify | Complex tables | Use concise lists |
| Extract | Repetitive structures | Create templates |
| Compact | Long code blocks | Essential parts only |

### Phase 3: Quality Gates

**MUST preserve**:
- [ ] Core functionality
- [ ] Essential context
- [ ] 1-2 examples
- [ ] Frontmatter (YAML + allowed-tools)
- [ ] Argument handling ($1)
- [ ] Command usability

### Phase 4: Delegate
- Reference `@docs` instead of embedding
- Suggest sub-commands for complex flows
- Point to MCP tools vs explaining them

### Phase 5: Output Report

```markdown
## Reduction Results

**Original**: ~X tokens → **Optimized**: ~Y tokens (**Z% reduction**)

### Changes
- [Specific optimizations applied]

### Quality Preserved
- [What remains functional]

### Usage
`/command-name [args]`

Example: [one concrete example]
```

## Guidelines

✓ **DO**: Remove filler, use imperative mood, consolidate, reference @docs
✗ **DON'T**: Break functionality, remove all examples, alter $1 handling

## Example

**BEFORE** (verbose):
```markdown
## Introduction
This command helps you create a feature branch using Git Flow...
[5+ lines of explanation]
```

**AFTER** (concise):
```markdown
Create Git Flow feature branch.

1. Check: `git status`
2. Create: `git checkout -b feature/$1`
3. Verify: `git branch`

Usage: `/feature-branch branch-name`
```

## Execution

1. Read command at **$1**
2. THINK HARD about optimization
3. Apply reductions preserving quality
4. Write optimized version
5. Report metrics

---

**One-shot optimization following HOP pattern. Read, analyze, reduce, output.**
