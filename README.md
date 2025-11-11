# Skill Forge

[English](README.md) | [中文](README.zh.md)

An automated skill creation workshop for Claude Code that transforms external resources (GitHub repositories, online documentation, PDFs) into well-structured, reusable skills.

## Features

- **🔍 Smart Source Detection** - Automatically identifies and fetches from GitHub, documentation sites, or local files
- **📦 Zero Configuration** - Works out of the box, no complex setup required
- **🆕 llms.txt Support** - Detects and uses llms.txt format for 10x faster documentation fetching
- **📄 Multi-Format Support** - Handles HTML docs, PDFs, Office documents (DOCX/PPTX/XLSX) via markitdown
- **🗂️ Intelligent Path Management** - Auto-detects project vs global mode for materials storage
- **✨ Progressive Disclosure** - Three-level loading system (metadata → SKILL.md → bundled resources)
- **🧹 Cleanup Tools** - Automatic cleanup management for temporary materials

## What Are Skills?

Skills are modular packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" that transform Claude from a general-purpose agent into a specialized expert.

### Skill Structure

```
skill-name/
├── SKILL.md          # Required: Instructions and metadata
├── scripts/          # Optional: Executable tools (Python/Bash)
├── references/       # Optional: Documentation loaded as needed
└── assets/           # Optional: Templates, images, boilerplate
```

## Installation

### Option 1: Download Release (Recommended)

1. Download `skill-forge.zip` from [Releases](https://github.com/WilliamSaysX/skill-forge/releases)
2. Extract to your skills directory:
   ```bash
   # For global skills (available everywhere)
   unzip skill-forge.zip -d ~/.claude/skills/

   # For project skills (current project only)
   unzip skill-forge.zip -d .claude/skills/
   ```

### Option 2: Git Clone

```bash
# Global installation
git clone https://github.com/WilliamSaysX/skill-forge ~/.claude/skills/skill-forge

# Project installation
git clone https://github.com/WilliamSaysX/skill-forge .claude/skills/skill-forge
```

## Requirements

- **Python 3.8+**
- **git** (for fetching GitHub repositories)
- **markitdown** (for documentation/PDF conversion):
  ```bash
  pip install 'markitdown[all]'
  ```

## Quick Start

### Example 1: Create Skill from GitHub Repository

```
You: Create a skill from https://github.com/joaomdmoura/crewAI
```

Claude will:
1. Auto-detect it's a GitHub repo
2. Clone repository to temp-materials/
3. Guide you through creating the skill
4. Install to ~/.claude/skills/crewai/ (ready to use!)
5. Optionally package as crewai.zip for sharing

### Example 2: Create Skill from Documentation

```
You: Turn https://docs.crewai.com/ into a skill
```

Claude will:
1. Check for llms.txt (10x faster)
2. Fetch documentation to temp-materials/
3. Help organize into skill structure
4. Install to skills directory (ready to use!)
5. Optionally create .zip for distribution

### Example 3: Create Skill from PDF

```
You: Create a skill from /path/to/manual.pdf
```

Claude will:
1. Convert PDF to markdown
2. Guide skill creation
3. Install to skills directory (ready to use!)
4. Optionally package for sharing

## Workflow Overview

1. **Fetch Materials** - Automatically fetch from GitHub/docs/PDF to temp-materials/
2. **Understand Purpose** - Clarify skill goals through examples
3. **Plan Contents** - Identify scripts, references, assets to bundle
4. **Initialize Skill** - Create skill in ~/.claude/skills/ or .claude/skills/
5. **Edit Skill** - Implement resources and write SKILL.md
6. **✅ Ready to Use** - Skill is installed and available immediately
7. **Package** - (Optional) Create .zip for sharing with others

## Supported Source Types

| Source Type | Example | Auto-Detection |
|-------------|---------|----------------|
| GitHub Repository | `github.com/user/repo` | ✅ Yes |
| Documentation Sites | `docs.example.com` | ✅ Yes |
| llms.txt | `docs.site.com/llms.txt` | ✅ Auto-detected |
| PDF Files | `example.com/doc.pdf` or `/path/to/file.pdf` | ✅ Yes |
| Office Documents | `.docx`, `.pptx`, `.xlsx` | ✅ Yes |
| Local Directories | `~/my-project/` | ✅ Yes |

## Path Management

skill-forge intelligently manages paths:

- **Materials** (temporary): Auto-saved to `.claude/temp-materials/` or `~/skill-materials/`
- **Skills** (permanent): You choose location (project or global)
- **Packages** (.zip): Created inside skill directory

## Documentation

Full documentation is available in SKILL.md and reference files:

- **[SKILL.md](SKILL.md)** - Complete usage guide for Claude
- **[workflow-guide.md](references/workflow-guide.md)** - Detailed step-by-step workflow
- **[source-detection.md](references/source-detection.md)** - Source type detection patterns
- **[path-management.md](references/path-management.md)** - Smart path management strategies
- **[popular-frameworks.md](references/popular-frameworks.md)** - Quick reference for 13 popular frameworks

## Scripts

- **`fetch_source.py`** - Fetch materials from Git/docs/PDF
- **`detect_llms_txt.py`** - Detect llms.txt availability
- **`init_skill.py`** - Initialize skill directory structure
- **`package_skill.py`** - Validate and package skills
- **`cleanup_materials.py`** - Clean up temporary materials

## Contributing

Issues and pull requests are welcome! Please ensure:

1. Skills follow the standard structure (SKILL.md + optional bundled resources)
2. Scripts include clear usage documentation
3. Changes maintain zero-configuration philosophy

## License

See [LICENSE.txt](LICENSE.txt) for complete terms.

## Acknowledgments

- Built upon [skill-creator](https://modelcontextprotocol.io/examples#skill-creator) from Anthropic's official Claude Code templates
- Inspired by [Skill Seekers](https://github.com/QuantGeekDev/skill-seekers)
- Built for [Claude Code](https://claude.com/claude-code)
- Uses [markitdown](https://github.com/microsoft/markitdown) for document conversion
- Supports [llms.txt](https://llmstxt.org/) standard for optimized documentation

---

**Made for AI agents, by humans (with AI assistance)**
