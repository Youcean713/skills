# SKILL.md Generation Rules

## Goal

Transform structured interview answers (`interview-answers.yaml`) into a complete 8-section SKILL.md.

## Generation Process

1. Load `interview-answers.yaml`
2. Fill the Jinja2 template `assets/templates/skill-md-template.md` for first pass
3. AI polishes: expand terse descriptions, ensure natural flow, add domain-specific nuance
4. Present to user for review

## Section Derivation Rules

### 1. Operating Model

- `evidence_label`: derived from input materials (e.g., "需求文档和测试用例" → "需求追溯证据")
- `delivery_label`: derived from core deliverables (e.g., "覆盖率报告生成")
- `governance_items`: standard set — workflow state, material inventory, blocker reports, user decisions
- `delivery_items`: from `core_deliverables` in interview answers

### 2. Required Workflow

- Directly from `workflow_phases` in interview answers
- Always append the `stop_and_report` note as the final sentence
- Each phase gets one sentence description from the interview data

### 3. Phase + Status State Model

- `phase` values: all phase names from `workflow_phases`
- `status` values: standard 6 (pending, in_progress, blocked, needs_review, done, deprecated)
- Include blocker format YAML example
- Include legal rollback table derived from phase dependencies

### 4. Decision Tree

Derived from phase dependency analysis:
- If a phase requires material X → "If X is missing, do not proceed to phase Y"
- If user provides new material → "Return to phase Z"
- Priority order: intake checks → blocker checks → continuation checks

### 5. Hard Rules

Reverse-derived from:
- Quality gates: each gate → at least one rule
- Blocker conditions: each blocker → a rule preventing the blocked action
- Domain common sense: standard rules from the workbench pattern (don't skip logging, don't hide blockers, etc.)

### 6. Resource Map

Generated from:
- Each workflow phase → at least one reference/ entry
- Each script in `scripts/` → one entry
- Standard governance entries (stop-and-report, state-management)

### 7. Quality Gates

Directly from `quality_gates` in interview answers, expanded with standard workbench gates:
- All config files exist and are internally consistent
- Every major claim has a source in the evidence directory
- Deliverables exist in the output directory
- Workflow logs reflect current phase and status

### 8. Delivery Contract

From `core_deliverables` and `output_dir_name` in interview answers.
Format: each deliverable on its own line with path relative to output directory.

## AI Polish Checklist

After template filling, verify:
- [ ] No template syntax remains (no `{{ }}` or `{% %}`)
- [ ] All paths use correct directory names from interview answers
- [ ] Phase descriptions are full sentences, not fragments
- [ ] Hard rules are specific to the domain, not generic
- [ ] Decision tree branches are actionable (if X → do Y)
