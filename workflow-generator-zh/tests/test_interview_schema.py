"""
采访 schema 的合约测试。
"""
import yaml
import pytest
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "templates"


def test_interview_schema_exists():
    """Schema 文件必须存在。"""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    assert schema_path.exists(), f"缺失：{schema_path}"


def test_interview_schema_valid_yaml():
    """Schema 必须是有效的 YAML，并包含必需的一级键。"""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    with open(schema_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert "layers" in data, "Schema 必须包含 'layers' 键"
    assert len(data["layers"]) == 3, "Schema 必须定义 3 层采访"
    layer_names = [layer["name"] for layer in data["layers"]]
    assert "domain_positioning" in layer_names
    assert "workflow_structure" in layer_names
    assert "detail_filling" in layer_names


def test_interview_schema_layer_2_has_all_dimensions():
    """第二层必须覆盖全部 6 个工作流结构维度。"""
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
        assert r in dimensions, f"第二层缺少维度：{r}"


def test_each_dimension_has_suggest_template():
    """每个维度必须有一个 suggest_template 供 AI 填写。"""
    schema_path = ASSETS_DIR / "interview-schema.yaml"
    with open(schema_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    for layer in data["layers"]:
        for dim in layer.get("dimensions", []):
            assert "suggest_template" in dim, \
                f"维度 {dim['name']} 缺少 suggest_template"
