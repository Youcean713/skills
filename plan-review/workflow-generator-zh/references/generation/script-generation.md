# 脚本生成规则

## 目标

基于交付物格式和工具链要求，为 Skill 生成 `scripts/` 目录和可执行 Python 脚本。

## 标准脚本（始终生成）

| 脚本 | 用途 |
| --- | --- |
| `workspace/init_workspace.py` | 初始化治理侧目录结构 |
| `workspace/check_workspace.py` | 验证工作区完整性 |

## 领域特定脚本（从交付物格式生成）

### 格式到库的映射

| 交付物格式 | Python 库 | 脚本模式 |
| --- | --- | --- |
| `.xlsx` | `openpyxl` | 数据 → pandas DataFrame → 带格式的 Excel（含多个工作表） |
| `.docx` | `python-docx` | Markdown → python-docx（含标题/段落样式） |
| `.json` | `json`（标准库） | Dict/List → json.dump（带缩进） |
| `.html` | `jinja2` | 数据 → Jinja2 模板 → HTML 文件 |
| `.csv` | `csv`（标准库） | 数据 → csv.writer |
| `.png`/`.jpg` | `matplotlib` 或 `Pillow` | 数据 → 图表/图片 → 文件 |

### 脚本命名规范

`scripts/<domain>/<verb>_<object>.py`

示例：
- `scripts/coverage/calculate_coverage.py`（计算覆盖率）
- `scripts/evidence/extract_requirements.py`（提取需求）
- `scripts/report/generate_report_xlsx.py`（生成 Excel 报告）

## 脚本骨架模板

每个生成的脚本必须包含：

```python
"""
<一行用途说明>
"""
import sys
from pathlib import Path


def main():
    """入口函数。"""
    pass


if __name__ == "__main__":
    main()
```

## 生成规则

1. 脚本必须是语法正确的 Python（通过 `python -m py_compile`）
2. 每个脚本只做一件事（单一职责）
3. 脚本仅使用标准库 + `requirements.txt` 中的包
4. 脚本接受路径作为参数，不硬编码路径
5. 脚本将进度输出到 stdout，将错误输出到 stderr
