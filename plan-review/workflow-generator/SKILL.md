---
name: workflow-generator
description: >
  Use when the user wants to transform an idea, concept, or workflow requirement
  into a complete production workflow skill package. Triggers include: "turn this
  into a workflow", "create a workflow for X", "I have an idea for a workflow",
  "build a workbench for", "generate a skill from this idea", or any request to
  systematize a process into a structured workbench with governance and delivery sides.
---

# Workflow Generator

## Operating Model

Use the three-layer interview as the discovery layer, then use template-driven generation as the output layer. Treat the user's natural language idea as the starting material that must be refined into structured parameters before any code is generated.

The generator has two sides:

- Governance side: `generator-context/` stores interview state, domain analysis, workflow design, blocker reports, and user decisions.
- Delivery side: `<workflow-name>/` stores the generated skill package — SKILL.md, references/, scripts/, assets/, tests/, and README.md.
- User-facing visibility: `generator-context/workflow/user-dashboard.md` summarizes current progress, pending decisions, missing information, and the next recommended action. `generator-context/workflow/blocker-report.md` records the latest blocker, options, recommendation, and limited-continuation status. `generator-context/workflow/user-decisions.md` records user-approved choices that affect the workflow design.

## Required Workflow

Run the workflow in this order:

1. `intake_idea`: Collect the user's natural language idea description.
2. `domain_analysis`: Analyze domain features — inputs, outputs, steps, constraints, tools. Present domain inference to user for confirmation.
3. `gap_interview`: Conduct three-layer interview (domain positioning → workflow structure → detail filling). AI suggests, user chooses.
4. `design_workflow`: Design the workflow skeleton — phase sequence, decision tree, hard rules, resource map.
5. `generate_skll_md`: Generate the core SKILL.md from interview answers. **HARD GATE — user must confirm before proceeding.**
6. `review_skll`: User reviews and adjusts SKILL.md.
7. `generate_references`: Generate references/ reference docs framework based on resource map.
8. `generate_scripts`: Generate scripts/ key scripts based on deliverable formats and tool chain.
9. `generate_assets`: Generate assets/ templates and configurations.
10. `generate_tests`: Generate tests/ contract tests from hard rules and quality gates.
11. `generate_readme`: Generate README.md usage documentation.
12. `quality_gates`: Run check_generated_skill.py to verify completeness, consistency, and syntax.
13. `delivery_report`: Report outputs, limitations, remaining human decisions, and verification evidence.
14. `archive_generation`: Archive generation records to generator-context/.

`stop_and_report` is a global blocking mechanism, not just a single step. Read `references/workflow/stop-and-report.md` whenever continuing may require guessing.

## Phase + Status State Model

Use this two-layer state model in `generator-context/workflow/workflow-status.md`, and mirror the user-facing summary in `generator-context/workflow/user-dashboard.md`:

| Field | Allowed values |
| --- | --- |
| `phase` | `intake_idea`, `domain_analysis`, `gap_interview`, `design_workflow`, `generate_skll_md`, `review_skll`, `generate_references`, `generate_scripts`, `generate_assets`, `generate_tests`, `generate_readme`, `quality_gates`, `delivery_report`, `archive_generation` |
| `status` | `pending`, `in_progress`, `blocked`, `needs_review`, `done`, `deprecated` |

When status becomes `blocked`, write `blocked_reason`, `missing_information`, `next_action`, and `can_continue_with_limitations` in the status file. Do not hide blockers in chat only.

After any meaningful phase, blocker, decision, or delivery-scope change, update `user-dashboard.md` so the user can see:

- current phase and status
- completed work
- decisions waiting for user confirmation
- missing information and its impact
- next recommended action
- limited-continuation options, if any

## Decision Tree

1. If there is no `generator-context/`, run `scripts/workspace/init_generator_workspace.py`.
2. If the user's idea description is too vague (missing 2+ of: domain, inputs, outputs), do Layer 1 interview first.
3. If Layer 1 domain is not confirmed, do not start Layer 2 workflow structure interview.
4. If Layer 2 interview answers are incomplete, do not start SKILL.md generation.
5. If `interview-answers.yaml` is not confirmed, do not generate SKILL.md.
6. If SKILL.md is not user-approved, do not generate references/, scripts/, or tests/.
7. If the resource map references non-existent domains, stop and redesign the workflow.
8. If asked to generate scripts without confirmed deliverable formats, stop and return to `design_workflow`.
9. If quality gates fail, return to the affected generation phase.
10. If asked for final delivery, run quality gates and produce the delivery report.

## Hard Rules

- AI always suggests first, user confirms or modifies. Never present a blank form.
- Do not generate SKILL.md before the three-layer interview is complete or the user explicitly confirms there are no more questions.
- During intake, classify each input material as `required`, `strongly_recommended`, or `optional`, and explain the effect of each missing required or strongly recommended material.
- Record user-approved decisions in `user-decisions.md`.
- User-facing workflow files are decision aids only. They must not weaken quality gates or delivery checks.
- Do not generate workflow files before domain analysis and interview are complete.
- When information is insufficient, trigger `stop_and_report`; do not guess the user's intent.
- When blocked, classify the issue as `hard_blocker`, `limited_continue`, or `user_choice_needed`, then provide user options and a recommended path.
- `interview-answers.yaml` is the single entry point for workflow generation parameters.
- `SKILL.md` generation is a hard gate — it must be user-confirmed before any further generation.
- Do not invent features, steps, tools, or constraints the user did not describe or approve.
- All generated file paths must use forward slashes and be relative to the skill package root.
- Output filenames must be descriptive, not generic (`requirement-coverage-report.xlsx` not `report.xlsx`).
- If the generated package includes Python scripts, they must pass `python -m py_compile` before claiming completion.

## Resource Map

| Need | Resource |
| --- | --- |
| Intake and idea collection | `references/workflow/intake.md` |
| Three-layer interview | `references/workflow/interview-engine.md` |
| Blocking and stop/report | `references/workflow/stop-and-report.md` |
| Generation state management | `references/workflow/workflow-state-management.md` |
| Pre-delivery verification | `references/workflow/quality-gates.md` |
| SKILL.md generation rules | `references/generation/skill-template.md` |
| Reference doc generation | `references/generation/reference-generation.md` |
| Script generation | `references/generation/script-generation.md` |
| Test generation | `references/generation/test-generation.md` |
| Workspace initialization | `scripts/workspace/init_generator_workspace.py` |
| Skill validation | `scripts/workspace/check_generated_skill.py` |
| SKILL.md generation tool | `scripts/generation/generate_skill_md.py` |
| Directory scaffolding | `scripts/generation/scaffold_directories.py` |
| SKILL.md template | `assets/templates/skill-md-template.md` |
| Interview schema | `assets/templates/interview-schema.yaml` |
| README template | `assets/templates/readme-template.md` |
| Reference template | `assets/templates/reference-template.md` |

## Quality Gates

Before claiming delivery quality, check:

- `interview-answers.yaml` has all Layer 2 dimensions filled and confirmed.
- SKILL.md has all 8 required sections present and domain-specific.
- YAML frontmatter is valid: `name` uses hyphens, `description` starts with "Use when...", total under 1024 chars.
- Every resource map entry points to an existing file in `references/`, `scripts/`, or `assets/`.
- Every hard rule is backed by at least one quality gate or blocker condition.
- The generated package has required directories: `references/`, `assets/templates/`; `scripts/` and `tests/` are only generated when the workflow design requires them.
- If `scripts/` contains `.py` files, they must pass `python -m py_compile`.
- If `tests/` exists, it must pass `python -m pytest`.
- README.md exists with quick start, architecture, and verification sections.
- `user-dashboard.md` reflects the current phase, pending decisions, and next action.
- `blocker-report.md` reflects the latest blocker if status is blocked.

## Delivery Contract

Deliver the generated skill package under the user's project directory:

- `<workflow-name>/SKILL.md`
- `<workflow-name>/README.md`
- `<workflow-name>/requirements.txt`
- `<workflow-name>/references/workflow/`
- `<workflow-name>/references/standards/`
- `<workflow-name>/references/evidence/`
- `<workflow-name>/references/writing/`
- `<workflow-name>/references/delivery/`
- `<workflow-name>/scripts/` (if workflow design includes scripts)
- `<workflow-name>/assets/templates/`
- `<workflow-name>/tests/` (if workflow design includes tests)

Also deliver generation records under `generator-context/`:

- `generator-context/workflow/user-dashboard.md`
- `generator-context/workflow/workflow-status.md`
- `generator-context/workflow/domain-analysis.md`
- `generator-context/workflow/interview-answers.yaml`
- `generator-context/workflow/blocker-report.md`
- `generator-context/workflow/user-decisions.md`
- `generator-context/workflow/progress-log.md`

Report what was generated, what was verified, what could not be verified, and what still needs human confirmation. If verification cannot run, state the command and the reason.
