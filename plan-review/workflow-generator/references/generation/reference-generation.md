# Reference Generation Rules

## Goal

Generate the `references/` directory for a workflow skill based on the resource map and workflow phases.

## Directory Structure

Every generated workflow has these reference subdirectories:

```
references/
  workflow/       # Intake, state management, blockers, quality gates
  standards/      # Domain standards and constraints
  evidence/       # Evidence/data collection rules
  writing/        # Execution/drafting rules
  delivery/       # Output delivery rules
```

## Standard Files (Always Generated)

These files are adapted from the generator's own references, with domain-specific content:

| File | Source to adapt | Customization |
| --- | --- | --- |
| `workflow/intake.md` | Generator's `intake.md` | Replace "workflow idea" with domain-specific materials |
| `workflow/stop-and-report.md` | Generator's `stop-and-report.md` | Replace blocking conditions with domain-specific ones |
| `workflow/workflow-state-management.md` | Generator's `workflow-state-management.md` | Replace phase vocabulary, context dir name |
| `workflow/quality-gates.md` | Generator's `quality-gates.md` | Replace gates with domain-specific verification |

## Domain-Specific Files (Generated from Interview)

Each item in the resource map generates one reference file:

1. **If the need is about evidence/data**: create `evidence/<topic>.md`
2. **If the need is about standards/constraints**: create `standards/<topic>.md`
3. **If the need is about execution/drafting**: create `writing/<topic>.md`
4. **If the need is about output/delivery**: create `delivery/<topic>.md`

## File Template

Every reference file uses this structure (from `assets/templates/reference-template.md`):

```markdown
# {{ reference_title }}

用于 {{ purpose }}。

硬约束：
- constraint 1
- constraint 2

必须确认：
1. item 1
2. item 2
```

## Generation Rules

1. Only create files that have a corresponding entry in the resource map
2. Do not create empty or placeholder files
3. Each file must have at least one hard constraint and one must-confirm item
4. File content must be domain-specific, not generic
