# workflow-generator（中文版）

> 将思路自动转变为完整生产工作流的元技能（自举式工作台）

[![Skill Type](https://img.shields.io/badge/Claude-Skill-blue)](https://claude.ai)

---

## 定位

**workflow-generator** 不是简单的代码生成器。它是一个元工作台——以 `chinese-thesis-workbench` 为参考模型，用三层采访引擎提取结构化参数，用渐进式生成产出完整 Skill 包。

核心原则：**AI 建议，用户选择；先生成核心定义（SKILL.md），确认后再逐步展开**。

### 适合场景

- 有一个工作流思路但不知道如何结构化的开发者
- 想把重复性工作（测试、报表、巡检、部署……）标准化的团队
- 需要快速搭建领域工作台的 QA、运维、数据分析师
- 想创建符合工作台模式（治理侧 + 交付侧）的 Skill 的 Skill 作者

### 不适合场景

- 只需要写一个简单脚本的场景（直接写脚本更快）
- 完全没有输入输出定义的模糊想法（先用头脑风暴理清思路）

---

## 快速开始

### 1. 安装依赖

```powershell
pip install -r requirements.txt
```

### 2. 加载 Skill 并描述思路

在 Claude Code 中加载本 Skill 后，直接用自然语言描述你的思路：

> "我需要一个根据需求文档和设计文档来计算测试覆盖率的工作流"

AI 会启动三层采访：
1. 确认领域定位
2. 对每个维度给出建议（输入材料、工作流阶段、目录名、交付物、质量门禁）
3. 补充追问缺口

### 3. 审查生成的 SKILL.md

采访完成后，AI 先生成 SKILL.md。这是**阻断点**——核心定义必须确认后才继续。

### 4. 渐进式展开

确认 SKILL.md 后，AI 逐步生成：
- `references/` 参考文档框架
- `scripts/` 可执行脚本
- `tests/` 合约测试
- `README.md` 使用文档

### 5. 质量验证

```powershell
python scripts/workspace/check_generated_skill.py <生成的Skill目录>
```

---

## 生成的工作流包结构

```
<workflow-name>/
  SKILL.md              # 8 段路由入口
  README.md
  requirements.txt
  references/           # 按需加载的参考文档
  scripts/              # 可执行工具
  assets/templates/     # 模板和配置
  tests/                # 合约测试
```

运行时生成：

```
<context-dir>/          # 治理侧：状态追踪、阻断管理、用户决策
<output-dir>/           # 交付侧：最终产出物
```

---

## 架构

```
治理侧 generator-context/
  workflow/         采访状态、领域分析、阻断报告、用户决策、进度日志

交付侧 <workflow-name>/
  SKILL.md          核心路由入口
  references/       按域组织的参考文档
  scripts/          可执行脚本
  assets/           模板资产
  tests/            合约测试
```

---

## 依赖

| 包 | 用途 |
| --- | --- |
| `pyyaml` | YAML 配置读写（interview-answers.yaml、interview-schema.yaml） |
| `jinja2` | SKILL.md 和 README 模板渲染 |
| `pytest` | 合约测试执行 |

---

## 验证

```powershell
# Python 编译检查
python -m compileall scripts tests

# 单元测试
python -m pytest tests/ -v

# 手动验证生成的 Skill
python scripts/workspace/check_generated_skill.py <path-to-generated-skill>
```

---

## 区分

本 Skill 是 workflow-generator 的中文版本。英文版请使用 `workflow-generator/`。

---

## 参考模型

| 项目 | 角色 |
| --- | --- |
| **chinese-thesis-workbench** | 工作台架构参考：治理侧+交付侧、阶段状态模型、决策树、硬规则、质量门禁、交付合约 |

---

## 许可

MIT License
