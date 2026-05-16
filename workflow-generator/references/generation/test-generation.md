# Test Generation Rules

## Goal

Generate contract tests for the workflow skill based on hard rules and quality gates.

## Test Derivation

### From Hard Rules

Each hard rule → at least one test:

```python
def test_<rule_summary_snake_case>():
    """<hard rule text>"""
    # Test that the rule is enforced
    pass
```

### From Quality Gates

Each quality gate → at least one test:

```python
def test_<gate_summary_snake_case>():
    """<quality gate text>"""
    # Test that the gate can be verified
    pass
```

### From Deliverables

Each deliverable → an existence/format test:

```python
def test_<deliverable_name>_contract():
    """<deliverable> must exist in <output_dir>/"""
    pass
```

## Test File Structure

```python
"""
Contract tests for <workflow-name> skill.
"""
import pytest
from pathlib import Path


# Path fixtures
# Contract tests for hard rules
# Contract tests for quality gates
# Contract tests for deliverables
```

## Generation Rules

1. Tests must be runnable with `python -m pytest`
2. Tests that require the generated context (governance/delivery dirs) use `pytest.mark.skipif` when dirs don't exist
3. Each test has a descriptive docstring referencing the rule/gate/deliverable it checks
4. Tests use Pathlib, not string paths
