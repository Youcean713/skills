# 测试生成规则

## 目标

基于硬规则和质量门禁，为 Skill 生成合约测试。

## 测试推导

### 从硬规则推导

每条硬规则 → 至少一个测试：

```python
def test_<规则摘要_蛇形命名>():
    """<硬规则文本>"""
    # 测试规则是否被强制执行
    pass
```

### 从质量门禁推导

每个质量门禁 → 至少一个测试：

```python
def test_<门禁摘要_蛇形命名>():
    """<质量门禁文本>"""
    # 测试门禁是否可被验证
    pass
```

### 从交付物推导

每个交付物 → 一个存在性/格式测试：

```python
def test_<交付物名>_contract():
    """<交付物> 必须存在于 <output_dir>/ 中"""
    pass
```

## 测试文件结构

```python
"""
<workflow-name> Skill 的合约测试。
"""
import pytest
from pathlib import Path


# 路径夹具（Path fixtures）
# 硬规则的合约测试
# 质量门禁的合约测试
# 交付物的合约测试
```

## 生成规则

1. 测试必须能用 `python -m pytest` 运行
2. 需要生成上下文（治理/交付目录）的测试，在目录不存在时使用 `pytest.mark.skipif`
3. 每个测试有一个描述性文档字符串，引用其检查的规则/门禁/交付物
4. 测试使用 Pathlib，不使用字符串路径
