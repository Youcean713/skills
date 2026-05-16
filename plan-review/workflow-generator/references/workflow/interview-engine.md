# Interview Engine

## Goal

Transform a user's natural language idea into structured workflow parameters using a three-layer interview model. The AI always suggests first, then the user confirms or modifies.

## Three-Layer Model

### Layer 1: Domain Positioning

**Purpose:** Confirm what domain this idea belongs to.

**Rule:** From the user's description, infer the domain label, purpose, and user persona. Present your inference as a suggestion. Do not proceed until the user confirms.

**Template:**
> Based on your description, this appears to be a **{domain_label}** workflow. It focuses on {domain_purpose}. Is this correct?

**Output:** `generator-context/workflow/domain-analysis.md`

**Red flags — do NOT proceed if:**
- The user's description is too vague to infer any domain
- The user rejects your suggestion but doesn't provide an alternative
- The user describes multiple unrelated domains

### Layer 2: Workflow Structure

**Purpose:** Define the workflow skeleton — inputs, phases, skill package name, deliverables, quality gates.

**Rule:** For each of the 5 dimensions, provide a concrete suggestion based on domain knowledge. Present one dimension at a time. Do not skip dimensions the user might not care about — suggest defaults and let them accept.

**Five dimensions (present in this order):**

1. **Input Materials** — Classify each as `required`, `strongly_recommended`, or `optional`. For each, explain what happens if it's missing.

2. **Workflow Phases** — Propose 7-14 ordered steps. Each step must have clear inputs and outputs. The last two steps are always `quality_gates` and `delivery_report`.

3. **Skill Package Name** — The generated skill package directory name, i.e. the delivery-side directory. Suggest based on workflow purpose (e.g., `test-coverage-analyzer`, `code-review-assistant`, `pipeline-runner`). Follow lowercase-hyphen naming. Note: the governance directory `generator-context/` is a fixed name used by the generator itself — it does not need user naming and must NOT be placed inside the generated skill package.

4. **Core Deliverables** — List with filenames and formats. Filenames should be descriptive, not generic (`需求覆盖率报告.xlsx` not `report.xlsx`).

5. **Quality Gates** — Each must be verifiable. Include verification method: `script` (automated), `manual` (human review), `format_check` (schema validation).

**Output:** `generator-context/workflow/interview-answers.yaml`

**Red flags:**
- User says "I don't know" to more than 2 dimensions — suggest concrete examples
- User wants fewer than 5 phases — explain why decomposition matters
- User rejects the lowercase-hyphen naming convention — explain skill package naming standards

### Layer 3: Detail Filling

**Purpose:** Fill gaps identified during Layer 2 — edge cases, error handling, domain-specific constraints.

**Rule:** Only trigger when gaps actually exist. Do not ask questions that Layer 2 already answered. Maximum 3 rounds.

**Trigger conditions:**
- Ambiguous input format description
- Unclear error handling preference
- Missing tool chain dependency
- Conflicting constraints

**Output:** Merged into `interview-answers.yaml`

**Red flags:**
- Asking a question that was already answered — re-read interview-answers.yaml first
- More than 3 rounds of detail questions — escalate to stop_and_report
