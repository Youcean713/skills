# Workflow State Management

## Goal

Create a generator workbench under `generator-context/workflow/` so the agent can resume work without guessing.

## Bootstrap

Run:

```powershell
python scripts/workspace/init_generator_workspace.py .
```

## Generated Files

| File | Purpose |
| --- | --- |
| `user-dashboard.md` | User-facing snapshot of progress, pending decisions, missing information, and next action |
| `workflow-status.md` | Current phase, next action, overall status |
| `progress-log.md` | Chronological generation-session log |
| `domain-analysis.md` | Domain positioning result from Layer 1 interview |
| `interview-answers.yaml` | Structured interview answers from Layer 2 |
| `blocker-report.md` | Latest blocker, affected scope, user options, recommendation |
| `user-decisions.md` | User-approved choices affecting workflow design, naming, deliverables, quality gates |

## Update Rules

At the start of a generation task:

1. Read `workflow-status.md`
2. Read `user-dashboard.md`
3. Read `blocker-report.md` when status is blocked
4. Read `user-decisions.md` when the request depends on prior user choices

At the end of a generation task:

1. Update `user-dashboard.md` with user-visible progress
2. Update `blocker-report.md` when work is blocked
3. Update `user-decisions.md` when user approves a choice
4. Append an entry to `progress-log.md`
5. Update `workflow-status.md` phase and status

## Status Vocabulary

- `pending`: not started
- `in_progress`: currently being worked on
- `blocked`: cannot proceed without information or decision
- `needs_review`: generated but needs user review
- `done`: verified enough for the current phase
- `deprecated`: no longer used

## Phase Vocabulary

- `intake_idea`
- `domain_analysis`
- `gap_interview`
- `design_workflow`
- `generate_skll_md`
- `review_skll`
- `generate_references`
- `generate_scripts`
- `generate_assets`
- `generate_tests`
- `generate_readme`
- `quality_gates`
- `delivery_report`
- `archive_generation`

## Legal Rollback Table

| Current phase | Trigger event | Target phase |
| --- | --- | --- |
| `review_skll` | User changes workflow phases | `design_workflow` |
| `generate_references` | User changes resource map | `design_workflow` |
| `generate_scripts` | User changes deliverable format | `design_workflow` |
| `generate_tests` | User adds/changes hard rules | `generate_skll_md` |
| `quality_gates` | Verification fails | affected generation phase |

## Non-Negotiable Rule

Do not silently skip log updates after changing generation state. The workbench is the memory of the generation project.

## User Dashboard Rules

Keep `user-dashboard.md` short enough for the user to scan before making decisions.

It should answer five questions:

1. Where are we in the generation process?
2. What has already been generated?
3. What does the user need to decide?
4. What information is missing, and what does it affect?
5. What is the next recommended action?
