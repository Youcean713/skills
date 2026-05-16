# Quality Gates

## Goal

Verify that a generated workflow skill package is complete, consistent, and ready for use before claiming delivery.

## Gates

### 1. SKILL.md Completeness

Check that SKILL.md has all 8 required sections:
- Operating Model
- Required Workflow
- Phase + Status State Model
- Decision Tree
- Hard Rules
- Resource Map
- Quality Gates
- Delivery Contract

### 2. YAML Frontmatter Validity

- `name` field uses letters, numbers, hyphens only
- `description` field starts with "Use when..."
- `description` field is written in third person
- Total frontmatter under 1024 characters

### 3. Resource Map Link Validity

Every path in the Resource Map table must point to an existing file in `references/` or `scripts/`.

### 4. Decision Tree Coverage

Every workflow phase must appear in at least one decision tree branch. The decision tree must cover: start conditions, blocking conditions, and continuation conditions.

### 5. Hard Rules Completeness

Every quality gate must be backed by at least one hard rule. Every blocker condition must have a corresponding hard rule.

### 6. Directory Integrity

The generated package must contain:
- `SKILL.md`
- `README.md`
- `references/` (non-empty)
- `scripts/` (non-empty)
- `assets/templates/` (non-empty)
- `tests/` (non-empty)

### 7. Script Syntax Check

Every `.py` file in `scripts/` must pass `python -m py_compile`.

### 8. Test Execution

All tests in `tests/` must pass with `python -m pytest`.

## Verification Command

```powershell
python scripts/workspace/check_generated_skill.py <generated-skill-path>
```

## Gate Failure Handling

| Gate | Failure action |
| --- | --- |
| SKILL.md completeness | Return to `generate_skll_md` |
| YAML validity | Fix frontmatter inline |
| Resource map links | Return to `generate_references` |
| Decision tree coverage | Return to `design_workflow` |
| Hard rules completeness | Return to `generate_skll_md` |
| Directory integrity | Return to `generate_scripts` or `generate_assets` |
| Script syntax | Fix script inline |
| Test execution | Return to `generate_tests` |
