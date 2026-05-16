# {{ skill_name }}

> {{ one_line_description }}

[![Skill Type](https://img.shields.io/badge/Claude-Skill-blue)](https://claude.ai)
{{ badges }}

---

## 定位

**{{ skill_name }}** {{ positioning_statement }}

核心原则：{{ core_principle }}

### 适合场景

{{ suitable_scenarios }}

### 不适合场景

{{ unsuitable_scenarios }}

---

## 快速开始

```powershell
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 初始化工作区
python scripts/workspace/{{ init_script }} <你的项目目录>

# 3. 编辑配置
#    <项目目录>/{{ context_dir }}/standards/...

# 4. 在 Claude Code 中加载本 Skill，告诉 AI：
#    "{{ example_prompt }}"
```

---

## 核心能力

### 治理侧

| 能力 | 说明 |
| --- | --- |
{% for cap in governance_capabilities %}
| {{ cap.name }} | {{ cap.description }} |
{% endfor %}

### 交付侧

| 能力 | 说明 |
| --- | --- |
{% for cap in delivery_capabilities %}
| {{ cap.name }} | {{ cap.description }} |
{% endfor %}

### 用户可见性

工作流初始化后在 `{{ context_dir }}/workflow/` 下生成控制文件：

| 文件 | 作用 |
| --- | --- |
{% for file in user_visible_files %}
| `{{ file.name }}` | {{ file.purpose }} |
{% endfor %}

---

## 架构

```
治理侧 {{ context_dir }}/
  workflow/         {{ governance_workflow_desc }}
  evidence/         {{ governance_evidence_desc }}
  standards/        {{ governance_standards_desc }}

交付侧 {{ output_dir }}/
  {{ delivery_structure }}
```

---

## 目录

```
{{ skill_name }}/
  SKILL.md                  Skill 路由入口
  README.md                 本文件
  requirements.txt          Python 依赖

  references/              按需加载的参考文档
    workflow/              {{ ref_workflow_desc }}
    standards/             {{ ref_standards_desc }}
    evidence/              {{ ref_evidence_desc }}
    writing/               {{ ref_writing_desc }}
    delivery/              {{ ref_delivery_desc }}

  scripts/                 可执行脚本
    workspace/             {{ scripts_workspace_desc }}
    evidence/              {{ scripts_evidence_desc }}

  assets/                  模板资产
    templates/             {{ assets_templates_desc }}

  tests/                   {{ tests_desc }}
```

---

## 依赖

| 包 | 用途 |
| --- | --- |
{% for dep in dependencies %}
| `{{ dep.package }}` | {{ dep.purpose }} |
{% endfor %}

---

## 验证

```powershell
# Python 编译检查
python -m compileall scripts tests

# 单元测试
python -m unittest discover tests

# 工作区模板校验
python scripts/workspace/check_workspace.py
```

---

## 许可

{{ license }}
