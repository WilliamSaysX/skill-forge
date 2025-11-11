# Skill Forge

[English](README.md) | [中文](README.zh.md)

一个自动化的 Claude Code 技能创建工具，可将外部资源（GitHub 仓库、在线文档、PDF）转换为结构良好、可复用的 Skill。

## 特性

- **🔍 智能源检测** - 自动识别并获取 GitHub、文档站点或本地文件
- **📦 零配置** - 开箱即用，无需复杂设置
- **🆕 支持 llms.txt** - 检测并使用 llms.txt 格式，文档获取速度提升 10 倍
- **📄 多格式支持** - 通过 markitdown 处理 HTML 文档、PDF、Office 文档（DOCX/PPTX/XLSX）
- **🗂️ 智能路径管理** - 自动检测项目模式或全局模式存储材料
- **✨ 渐进式加载** - 三级加载系统（元数据 → SKILL.md → 打包资源）
- **🧹 清理工具** - 自动管理临时材料清理

## 什么是 Skill？

Skill 是模块化的包，通过提供专业知识、工作流程和工具来扩展 Claude 的能力。可以把它们看作"入职指南"，将 Claude 从通用代理转变为专业专家。

### Skill 结构

```
skill-name/
├── SKILL.md          # 必需：指令和元数据
├── scripts/          # 可选：可执行工具（Python/Bash）
├── references/       # 可选：按需加载的文档
└── assets/           # 可选：模板、图片、样板代码
```

## 安装

### 方式 1：下载 Release（推荐）

1. 从 [Releases](https://github.com/USERNAME/skill-forge/releases) 下载 `skill-forge.zip`
2. 解压到你的 skills 目录：
   ```bash
   # 全局 skills（在任何地方可用）
   unzip skill-forge.zip -d ~/.claude/skills/

   # 项目 skills（仅当前项目）
   unzip skill-forge.zip -d .claude/skills/
   ```

### 方式 2：Git Clone

```bash
# 全局安装
git clone https://github.com/USERNAME/skill-forge ~/.claude/skills/skill-forge

# 项目安装
git clone https://github.com/USERNAME/skill-forge .claude/skills/skill-forge
```

## 环境要求

- **Python 3.8+**
- **git**（用于获取 GitHub 仓库）
- **markitdown**（用于文档/PDF 转换）：
  ```bash
  pip install 'markitdown[all]'
  ```

## 快速开始

### 示例 1：从 GitHub 仓库创建 Skill

```
你：从 https://github.com/joaomdmoura/crewAI 创建一个 skill
```

Claude 会：
1. 自动检测这是 GitHub 仓库
2. 克隆仓库
3. 引导你创建 skill
4. 打包为 `crewai.zip`

### 示例 2：从文档创建 Skill

```
你：把 https://docs.crewai.com/ 转成一个 skill
```

Claude 会：
1. 检查 llms.txt（速度快 10 倍）
2. 获取文档
3. 帮助组织成 skill 结构
4. 创建可分发的包

### 示例 3：从 PDF 创建 Skill

```
你：从 /path/to/manual.pdf 创建一个 skill
```

Claude 会：
1. 将 PDF 转换为 markdown
2. 引导 skill 创建
3. 打包资源

## 工作流程概览

1. **获取材料** - 自动从 GitHub/文档/PDF 获取
2. **理解目的** - 通过示例明确 skill 目标
3. **规划内容** - 识别要打包的脚本、参考文档、资源
4. **初始化 Skill** - 创建 skill 目录结构
5. **编辑 Skill** - 实现资源并编写 SKILL.md
6. **打包** - 验证并创建可分发的 .zip

## 支持的源类型

| 源类型 | 示例 | 自动检测 |
|--------|------|----------|
| GitHub 仓库 | `github.com/user/repo` | ✅ 是 |
| 文档站点 | `docs.example.com` | ✅ 是 |
| llms.txt | `docs.site.com/llms.txt` | ✅ 自动检测 |
| PDF 文件 | `example.com/doc.pdf` 或 `/path/to/file.pdf` | ✅ 是 |
| Office 文档 | `.docx`、`.pptx`、`.xlsx` | ✅ 是 |
| 本地目录 | `~/my-project/` | ✅ 是 |

## 路径管理

skill-forge 智能管理路径：

- **材料**（临时）：自动保存到 `.claude/temp-materials/` 或 `~/skill-materials/`
- **Skills**（永久）：由你选择位置（项目或全局）
- **包**（.zip）：在 skill 目录内创建

## 文档

完整文档在 SKILL.md 和参考文件中：

- **[SKILL.md](SKILL.md)** - Claude 的完整使用指南
- **[workflow-guide.md](references/workflow-guide.md)** - 详细的分步工作流程
- **[source-detection.md](references/source-detection.md)** - 源类型检测模式
- **[path-management.md](references/path-management.md)** - 智能路径管理策略
- **[popular-frameworks.md](references/popular-frameworks.md)** - 13 个流行框架的快速参考

## 脚本

- **`fetch_source.py`** - 从 Git/文档/PDF 获取材料
- **`detect_llms_txt.py`** - 检测 llms.txt 可用性
- **`init_skill.py`** - 初始化 skill 目录结构
- **`package_skill.py`** - 验证并打包 skills
- **`cleanup_materials.py`** - 清理临时材料

## 贡献

欢迎 Issues 和 Pull Requests！请确保：

1. Skills 遵循标准结构（SKILL.md + 可选的打包资源）
2. 脚本包含清晰的使用文档
3. 更改保持零配置理念

## 许可证

详见 [LICENSE.txt](LICENSE.txt)。

## 致谢

- 基于 Anthropic 官方 Claude Code 模板中的 [skill-creator](https://modelcontextprotocol.io/examples#skill-creator) 构建
- 灵感来自 [Skill Seekers](https://github.com/QuantGeekDev/skill-seekers)
- 为 [Claude Code](https://claude.com/claude-code) 构建
- 使用 [markitdown](https://github.com/microsoft/markitdown) 进行文档转换
- 支持 [llms.txt](https://llmstxt.org/) 标准以优化文档获取

---

**为 AI 代理而造，由人类（在 AI 协助下）创建**
