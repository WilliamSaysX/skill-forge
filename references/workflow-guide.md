# Skill Creation Workflow - Detailed Guide

Complete step-by-step guide for creating skills from any source.

## Overview

Follow these 6 steps to create an effective skill:

1. **Step 0**: Fetch Source Materials (Automatic)
2. **Step 1**: Understanding the Skill with Concrete Examples
3. **Step 2**: Planning the Reusable Skill Contents
4. **Step 3**: Initializing the Skill
5. **Step 4**: Edit the Skill
6. **Step 5**: Packaging a Skill
7. **Step 6**: Iterate

---

## Step 0: Fetch Source Materials (Automatic)

This step is automatically executed when the user provides an external source (GitHub URL or documentation URL). Skip this step only if source materials are already available locally.

### Smart Path Selection

Materials are stored in different locations depending on the context:

**Project Mode** (when inside a project with `.git` or `.claude/`):
- Materials path: `<project-root>/.claude/temp-materials/`
- Benefit: Tools like Trae can access materials within the project
- Example: `~/Workspace/my-project/.claude/temp-materials/repo-name/`

**Global Mode** (when outside any project):
- Materials path: `~/skill-materials/`
- Benefit: Doesn't clutter projects, shared across sessions
- Example: `~/skill-materials/repo-name/`

The mode is detected automatically. No configuration needed.

### From GitHub Repository

```bash
scripts/fetch_source.py --git https://github.com/user/awesome-tool
```

Options:
- `--depth 1` - Shallow clone (faster, smaller)
- `--branch <name>` - Clone specific branch
- `--single-branch` - Clone only one branch
- `--output <path>` - Custom output directory
- `--clean` - Clean existing directory first

Examples:

```bash
# Quick shallow clone
scripts/fetch_source.py --git https://github.com/user/repo --depth 1

# Specific branch
scripts/fetch_source.py --git https://github.com/user/repo --branch develop

# Custom location
scripts/fetch_source.py --git https://github.com/user/repo --output ~/my-materials/repo
```

### From Online Documentation

```bash
scripts/fetch_source.py --docs https://docs.example.com --name example-docs
```

The `--name` parameter is required for documentation sources.

### Combined: Repository + Documentation

```bash
scripts/fetch_source.py --git https://github.com/user/repo --docs https://docs.example.com --name combo
```

### After Fetching

Once materials are fetched, the script will show:
- Directory statistics (file counts, sizes)
- Suggested next steps
- Example prompts to give Claude

---

## Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

### Example Questions

For an image-editor skill:
- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

### Best Practices

- Avoid overwhelming users with too many questions in a single message
- Start with the most important questions
- Follow up as needed for better effectiveness
- Conclude when there is a clear sense of the functionality the skill should support

---

## Step 2: Planning the Reusable Skill Contents

Turn concrete examples into an effective skill by analyzing each example:

1. Consider how to execute on the example from scratch
2. Identify what scripts, references, and assets would be helpful when executing these workflows repeatedly

### Examples

**PDF Editor Skill**
- Query: "Help me rotate this PDF"
- Analysis: Rotating a PDF requires re-writing the same code each time
- Solution: A `scripts/rotate_pdf.py` script

**Frontend Webapp Builder Skill**
- Query: "Build me a todo app" or "Build me a dashboard to track my steps"
- Analysis: Writing a frontend webapp requires the same boilerplate HTML/React each time
- Solution: An `assets/hello-world/` template containing the boilerplate project files

**BigQuery Skill**
- Query: "How many users have logged in today?"
- Analysis: Querying BigQuery requires re-discovering the table schemas each time
- Solution: A `references/schema.md` file documenting the table schemas

### Output

Create a list of the reusable resources to include: scripts, references, and assets.

---

## Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed.

### Running init_skill.py

Always run the `init_skill.py` script to generate a new template skill directory:

```bash
scripts/init_skill.py <skill-name> --path <user-chosen-path>
```

### Choosing Skill Location

Unlike temporary materials (which use smart auto-detection), the skill itself is permanent and should be placed where the user prefers. Ask the user:

**Common choices:**

1. **Project-specific skill** (for this project only):
   - Path: `<project-root>/.claude/skills/`
   - Use when: Skill is tightly coupled to this project
   - Example: Project-specific API helpers, custom workflows

2. **Global skill** (available everywhere):
   - Path: `~/.claude/skills/`
   - Use when: Skill is generally useful across projects
   - Example: General utilities, common frameworks

3. **Custom location**:
   - Path: User-specified
   - Use when: Special organization needs

**Ask the user:**
```
Where would you like to create the <skill-name> skill?
1. Project skills (.claude/skills/) - For this project only
2. Global skills (~/.claude/skills/) - Available everywhere
3. Custom path - Specify your own location
```

### Examples

```bash
# Project-specific (user chose option 1)
scripts/init_skill.py crewai --path ./.claude/skills

# Global (user chose option 2)
scripts/init_skill.py crewai --path ~/.claude/skills

# Custom (user chose option 3)
scripts/init_skill.py crewai --path ~/my-skills
```

### What the Script Creates

- Skill directory at the specified path
- SKILL.md template with proper frontmatter and TODO placeholders
- Example resource directories: `scripts/`, `references/`, and `assets/`
- Example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

---

## Step 4: Edit the Skill

When editing the skill, remember that it is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude.

### Start with Reusable Skill Contents

Begin implementation with the reusable resources identified in Step 2: `scripts/`, `references/`, and `assets/` files.

Note: This step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill.

### Update SKILL.md

**Writing Style:** Use **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X").

Answer these questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

---

## Step 5: Packaging a Skill

Once the skill is ready, package it into a distributable zip file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

### The Packaging Process

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `crewai.zip`)

### Output Locations

**Default**: Creates `<skill-name>.zip` in the skill directory itself
- Example: `~/.claude/skills/crewai/crewai.zip`

**Custom output**: Specify a different directory for the zip file
```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```
- Example output: `./dist/crewai.zip`

### Complete Example

```bash
# Skill created at: ~/.claude/skills/crewai/
# Package it:
scripts/package_skill.py ~/.claude/skills/crewai/

# Result:
# ✅ Validation passed
# 📦 Created: ~/.claude/skills/crewai/crewai.zip
```

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

### Cleaning Up Source Materials

After successfully packaging the skill, consider cleaning up the temporary source materials fetched in Step 0. See [path-management.md](path-management.md) for detailed cleanup instructions.

---

## Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

### Iteration Workflow

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

### Common Iteration Triggers

- Skill struggles with certain edge cases
- User discovers additional use cases
- Performance improvements needed
- Documentation needs clarification
- New examples or patterns discovered

---

## See Also

- [path-management.md](path-management.md) - Detailed path management and cleanup
- [source-detection.md](source-detection.md) - Source detection rules and examples
