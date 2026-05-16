# 质量门禁

## 目标

验证生成的 Skill 包在声明交付之前是完整的、一致的和可用的。

## 门禁

### 1. SKILL.md 完整性

检查 SKILL.md 具备全部 8 个必需部分：
- 运营模型（Operating Model）
- 必需工作流（Required Workflow）
- 阶段 + 状态模型（Phase + Status State Model）
- 决策树（Decision Tree）
- 硬规则（Hard Rules）
- 资源映射（Resource Map）
- 质量门禁（Quality Gates）
- 交付合约（Delivery Contract）

### 2. YAML 前置元数据有效性

- `name` 字段仅使用字母、数字和连字符
- `description` 字段以"当……时使用"开头
- `description` 字段使用第三人称
- 前置元数据总计不超过 1024 字符

### 3. 资源映射链接有效性

资源映射表中的每个路径必须指向 `references/` 或 `scripts/` 中的现有文件。

### 4. 决策树覆盖度

每个工作流阶段必须出现在至少一个决策树分支中。决策树必须覆盖：启动条件、阻断条件和继续条件。

### 5. 硬规则完整性

每个质量门禁必须至少由一条硬规则支撑。每个阻断条件必须有对应的硬规则。

### 6. 目录完整性

生成的包必须包含：
- `SKILL.md`
- `README.md`
- `references/`（非空）
- `scripts/`（非空）
- `assets/templates/`（非空）
- `tests/`（非空）

### 7. 脚本语法检查

`scripts/` 中的每个 `.py` 文件必须通过 `python -m py_compile`。

### 8. 测试执行

`tests/` 中的所有测试必须通过 `python -m pytest`。

## 验证命令

```powershell
python scripts/workspace/check_generated_skill.py <生成的Skill路径>
```

## 门禁失败处理

| 门禁 | 失败处理 |
| --- | --- |
| SKILL.md 完整性 | 返回到 `generate_skll_md` |
| YAML 有效性 | 直接修复前置元数据 |
| 资源映射链接 | 返回到 `generate_references` |
| 决策树覆盖度 | 返回到 `design_workflow` |
| 硬规则完整性 | 返回到 `generate_skll_md` |
| 目录完整性 | 返回到 `generate_scripts` 或 `generate_assets` |
| 脚本语法 | 直接修复脚本 |
| 测试执行 | 返回到 `generate_tests` |
