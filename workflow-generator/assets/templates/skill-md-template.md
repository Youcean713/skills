---
name: {{ skill_name }}
description: {{ description }}
---

# {{ title }}

## Operating Model

Use {{ evidence_label }} as the control layer, then use the {{ delivery_label }} pipeline as the output layer. Treat {{ input_summary }} as materials that must be resolved into structured state before {{ output_action }}.

The workbench has two sides:

- Governance side: `{{ context_dir }}/` stores workflow state, {{ governance_items }}.
- Delivery side: `{{ output_dir }}/` stores {{ delivery_items }}.
- User-facing visibility: `{{ context_dir }}/workflow/user-dashboard.md` summarizes current progress, missing materials, user decisions needed, and the next recommended action. `{{ context_dir }}/workflow/content-decisions.md` records optional content emphasis and exclusion decisions. `{{ context_dir }}/workflow/blocker-report.md` records the latest blocker, options, recommendation, and limited-continuation status. `{{ context_dir }}/workflow/user-decisions.md` records user-approved choices.

## Required Workflow

Run the workflow in this order unless the user is only asking for a narrow task:

{% for phase in phases %}
{{ phase.order }}. `{{ phase.name }}`: {{ phase.description }}
{% endfor %}

`stop_and_report` is a global blocking mechanism, not just a single step. Read `references/workflow/stop-and-report.md` whenever continuing may require guessing.

## Phase + Status State Model

Use this two-layer state model in `{{ context_dir }}/workflow/workflow-status.md`, and mirror the user-facing summary in `{{ context_dir }}/workflow/user-dashboard.md`:

| Field | Allowed values |
| --- | --- |
| `phase` | {% for phase in phases %}`{{ phase.name }}`{% if not loop.last %}, {% endif %}{% endfor %} |
| `status` | `pending`, `in_progress`, `blocked`, `needs_review`, `done`, `deprecated` |

When status becomes `blocked`, write `blocked_reason`, `missing_materials`, `next_action`, and `can_continue_with_limitations` in the status file. Do not hide blockers in chat only.

After any meaningful phase, blocker, material, or delivery-scope change, update `user-dashboard.md` so the user can see:

- current phase and status
- completed work
- decisions waiting for user confirmation
- missing materials and their impact
- next recommended action
- limited-continuation options, if any

## Decision Tree

{% for decision in decision_tree %}
{{ decision.order }}. {{ decision.condition }}
{% endfor %}

## Hard Rules

{% for rule in hard_rules %}
- {{ rule }}
{% endfor %}

## Resource Map

| Need | Resource |
| --- | --- |
{% for resource in resource_map %}
| {{ resource.need }} | {{ resource.location }} |
{% endfor %}

## Quality Gates

Before claiming delivery quality, check:

{% for gate in quality_gates %}
- {{ gate }}
{% endfor %}

## Delivery Contract

Deliver artifacts under `{{ output_dir }}/`:

{% for deliverable in deliverables %}
- {{ deliverable }}
{% endfor %}

Report what was verified, what could not be verified, and what still needs human confirmation. If verification cannot run, state the command and the reason.
