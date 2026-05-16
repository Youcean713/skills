import yaml
import pytest
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "templates"


def test_interview_schema_exists():
    """Schema file must exist."""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    assert schema_path.exists(), f"Missing: {schema_path}"


def test_interview_schema_valid_yaml():
    """Schema must be valid YAML with required top-level keys."""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    with open(schema_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert "layers" in data, "Schema must have 'layers' key"
    assert len(data["layers"]) == 3, "Schema must define 3 interview layers"
    layer_names = [layer["name"] for layer in data["layers"]]
    assert "domain_positioning" in layer_names
    assert "workflow_structure" in layer_names
    assert "detail_filling" in layer_names


def test_interview_schema_layer_2_has_all_dimensions():
    """Layer 2 must cover all 6 workflow structure dimensions."""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    with open(schema_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    layer2 = [l for l in data["layers"] if l["name"] == "workflow_structure"][0]
    dimensions = [d["name"] for d in layer2["dimensions"]]
    required = [
        "input_materials", "workflow_phases", "context_dir_name",
        "output_dir_name", "core_deliverables", "quality_gates"
    ]
    for r in required:
        assert r in dimensions, f"Layer 2 missing dimension: {r}"


def test_each_dimension_has_suggest_template():
    """Every dimension must have a suggest_template for AI to fill."""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    with open(schema_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for layer in data["layers"]:
        for dim in layer.get("dimensions", []):
            assert "suggest_template" in dim, \
                f"Dimension {dim['name']} missing suggest_template"
