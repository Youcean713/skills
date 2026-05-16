# 个人 Skill 管理仓库

这是一个用于管理和组织个人 Claude Code Skill 的仓库。

## 目录结构

```
skills/
├── plan-review/                    # 方案互审工作流
├── workflow-generator/            # 工作流生成器（英文版）
├── workflow-generator-zh/         # 工作流生成器（中文版）
├── .gitignore                     # Git 忽略配置
└── README.md                      # 项目说明文档
```

## Skill 列表

### 1. 方案互审工作流 (plan-review)

**用途：** 调用 Claude Code 作为独立审查方，对当前生成的项目开发方案进行多轮结构化审查，直到方案通过。

**触发词：**
- "审查方案"、"检查方案"、"让 Claude 看一下方案"
- "review 一下计划"、"方案互审"、"plan review"
- "交叉验证"、"第二意见"、"独立审查"

**核心特性：**
- 多轮结构化审查机制
- 自动追踪迭代轮次
- 支持文件和文本输入
- 审查结果自动保存和回溯

**使用方式：**
```bash
python ".claude/skills/plan-review/assets/review.py" --file <方案文件路径>
# 或
python ".claude/skills/plan-review/assets/review.py" --text "方案内容"
```

---

### 2. 工作流生成器 (workflow-generator)

**用途：** 将用户的思路、概念或工作流需求转化为完整的产品级工作流 Skill 包。

**触发词：**
- "把这个变成工作流"、"为X创建一个工作流"
- "我有一个工作流的想法"、"构建一个工作台"
- "根据这个思路生成Skill"

**核心特性：**
- 三层采访发现机制
- 模板驱动生成
- 治理侧和交付侧分离
- 完整的质量门禁体系
- 自动生成 SKILL.md、references、scripts、assets、tests

**适用场景：** 英文用户或需要英文输出的工作流生成需求

---

### 3. 工作流生成器中文版 (workflow-generator-zh)

**用途：** 与英文版功能相同，专门面向中文用户提供本地化的工作流生成体验。

**触发词：**
- "把这个变成工作流"、"为X创建一个工作流"
- "我有一个工作流的想法"、"构建一个工作台"
- "根据这个思路生成Skill"

**核心特性：**
- 完整的中文界面和文档
- 符合中文用户习惯的交互方式
- 中文模板和示例

**适用场景：** 中文用户的工作流生成需求

---

## 使用建议

1. **方案审查：** 当你完成一个项目方案后，使用 `plan-review` 进行独立审查，确保方案质量
2. **工作流创建：** 当你有一个流程化的工作想法时，使用 `workflow-generator` 将其系统化为可复用的 Skill
3. **语言选择：** 根据你的语言偏好选择英文版或中文版的工作流生成器

## 维护说明

- 每个 Skill 都有独立的目录结构
- 包含 SKILL.md（核心定义）、references/（参考资料）、scripts/（脚本）、assets/（资源）、tests/（测试）
- 使用 Git 进行版本管理

## 更新日志

### 2026-05-16 (第二次更新)
- 修复项目结构：将三个 Skill 提升到根目录层级
- 添加 .gitignore 文件，排除 .claude/ 等本地配置
- 更新 README.md 反映正确的目录结构

### 2026-05-16 (第一次更新)
- 初始化仓库
- 添加 `plan-review` 方案互审工作流 Skill
- 添加 `workflow-generator` 工作流生成器（英文版）
- 添加 `workflow-generator-zh` 工作流生成器（中文版）
- 创建 README.md 项目说明文档
