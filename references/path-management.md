# Path Management and Cleanup - Detailed Guide

Complete guide to managing paths for source materials, skills, and packages.

## Overview

The skill-creator uses three distinct types of paths, each with its own management strategy:

| Type | Purpose | Location Strategy | Cleanup |
|------|---------|-------------------|---------|
| **Source Materials** | Temporary files fetched from git/docs | Auto-detected (smart) | Manual cleanup after skill creation |
| **Skill Directory** | Permanent skill files (SKILL.md, scripts/, etc.) | User chooses | Keep permanently |
| **Packaged Zip** | Distributable archive | Inside skill directory | Keep for distribution |

---

## Source Materials Paths

### Smart Auto-Detection

Source materials use intelligent path detection based on your current context. This happens automatically without configuration.

**Decision Logic:**

```
Are you inside a project directory?
├─ YES (.git or .claude/ found)
│  └─ Use: <project-root>/.claude/temp-materials/
│     Benefits:
│     - Tools like Trae can access the materials
│     - Materials stay with the project
│     - Easy cleanup when done with project
│
└─ NO (no project markers found)
   └─ Use: ~/skill-materials/
      Benefits:
      - Doesn't clutter any project
      - Shared across all sessions
      - Accessible from anywhere
```

### Project Mode

**When:** You're inside a project directory (contains `.git` or `.claude/`)

**Materials Location:** `<project-root>/.claude/temp-materials/<source-name>/`

**Example:**
```bash
# You're in: ~/Workspace/my-project/
# Fetch materials:
scripts/fetch_source.py --git https://github.com/user/awesome-tool

# Materials saved to:
# ~/Workspace/my-project/.claude/temp-materials/awesome-tool/
```

**Benefits:**
- Project-scoped tools (like Trae) can access materials
- Materials are co-located with related project code
- Automatic cleanup when project is deleted
- Clear association between materials and project

**Use Cases:**
- Creating project-specific skills
- Working with tools that can't access files outside the project
- Building skills that integrate with current project

### Global Mode

**When:** You're outside any project directory

**Materials Location:** `~/skill-materials/<source-name>/`

**Example:**
```bash
# You're in: ~/Downloads/ (no project)
# Fetch materials:
scripts/fetch_source.py --git https://github.com/user/awesome-tool

# Materials saved to:
# ~/skill-materials/awesome-tool/
```

**Benefits:**
- Doesn't clutter any specific project
- Accessible from anywhere on your system
- Shared across all Claude sessions
- Persists independently of projects

**Use Cases:**
- Creating general-purpose skills
- Working from non-project locations
- Building skills for global use

### Mode Detection Example

The `fetch_source.py` script shows which mode it's using:

```bash
$ cd ~/Workspace/my-project
$ scripts/fetch_source.py --git https://github.com/user/repo

📍 Project mode detected
   Project root: /Users/you/Workspace/my-project
   Materials will be saved in project: .claude/temp-materials/
```

```bash
$ cd ~/Downloads
$ scripts/fetch_source.py --git https://github.com/user/repo

📍 Global mode
   Materials will be saved in: ~/skill-materials/
```

### Overriding Auto-Detection

Use `--output` to specify a custom path:

```bash
# Force specific location regardless of mode
scripts/fetch_source.py --git https://github.com/user/repo --output ~/my-custom-materials/repo
```

---

## Skill Directory Paths

### User Choice (No Auto-Detection)

Unlike source materials, skills are permanent and should be placed where YOU prefer. Always ask the user.

**Three Standard Options:**

#### 1. Project Skills

**Path:** `<project-root>/.claude/skills/<skill-name>/`

**When to Use:**
- Skill is specific to this project only
- Skill contains project-specific helpers or workflows
- Skill integrates tightly with project codebase

**Example:**
```bash
# Creating a project-specific API helper skill
scripts/init_skill.py my-api --path ./.claude/skills
```

**Pros:**
- Co-located with relevant code
- Version controlled with project
- Clear project-skill association

**Cons:**
- Not available in other projects
- Duplicated if needed elsewhere

#### 2. Global Skills

**Path:** `~/.claude/skills/<skill-name>/`

**When to Use:**
- Skill is generally useful across many projects
- Skill provides common utilities or frameworks
- Skill should be available everywhere

**Example:**
```bash
# Creating a general-purpose tool skill
scripts/init_skill.py crewai --path ~/.claude/skills
```

**Pros:**
- Available in all projects and sessions
- Single source of truth
- Easy to update globally

**Cons:**
- Not version-controlled with specific projects
- May need project-specific customization

#### 3. Custom Path

**Path:** User-specified

**When to Use:**
- Special organization requirements
- Shared team directory
- Custom skill repository

**Example:**
```bash
# Using a custom skills directory
scripts/init_skill.py tool --path ~/my-team-skills
```

### How to Ask Users

**Recommended Prompt:**

```
Where would you like to create the <skill-name> skill?

1. Project skills (.claude/skills/) - For this project only
2. Global skills (~/.claude/skills/) - Available everywhere
3. Custom path - Specify your own location

Please choose 1, 2, or 3:
```

Then execute based on their choice:

```bash
# Option 1
scripts/init_skill.py <skill-name> --path ./.claude/skills

# Option 2
scripts/init_skill.py <skill-name> --path ~/.claude/skills

# Option 3
scripts/init_skill.py <skill-name> --path <user-provided-path>
```

---

## Package (.zip) Paths

### Default Location

The packaged zip file is created **inside the skill directory** by default:

```
~/.claude/skills/crewai/
├── SKILL.md
├── scripts/
├── references/
└── crewai.zip          ← Package created here
```

This keeps the distributable package with its source, making it easy to:
- Share the skill (just send the .zip)
- Rebuild if needed (source is right there)
- Version control both together

### Custom Package Location

Specify a different output directory:

```bash
# Package to a specific distribution directory
scripts/package_skill.py ~/.claude/skills/crewai/ ./dist

# Result:
# ./dist/crewai.zip
```

**Use Cases:**
- Publishing to a shared team directory
- Organizing all packages in one location
- CI/CD build artifacts directory

---

## Cleanup Strategies

### When to Clean Materials

**Default Strategy: Keep materials until manually cleaned**

Reasons to keep:
- May need to reference during iteration
- Useful for debugging skill behavior
- Source for future updates
- Low cost to storage

**When to Clean:**

1. **After successful packaging** - Skill is complete and tested
2. **Disk space constraints** - Materials are large
3. **Security concerns** - Materials contain sensitive data
4. **Project completion** - Done with the project entirely

### Using cleanup_materials.py

The cleanup script supports both project and global materials automatically.

#### List All Materials

```bash
scripts/cleanup_materials.py --list
```

**Example Output:**

```
📂 Source materials:

  📍 Project mode (/Users/you/Workspace/my-project/.claude/temp-materials/):
     1. awesome-tool                 15.3 MB
     2. docs-example                  2.1 MB

  🌍 Global mode (~/skill-materials/):
     3. crewai                       45.2 MB
     4. langchain                    67.8 MB

  Total: 4 projects, 130.4 MB
```

#### Interactive Cleanup

```bash
# Run without arguments for interactive mode
scripts/cleanup_materials.py

# Choose what to delete:
# - Specific item by number
# - 'all' to delete everything (with confirmation)
# - 'quit' to exit
```

#### Delete Specific Material

```bash
# Delete by name (searches both locations automatically)
scripts/cleanup_materials.py awesome-tool
```

The script will:
1. Search project mode location
2. Search global mode location
3. Delete from whichever location it's found
4. Ask for confirmation (unless --force)

#### Delete All Materials

```bash
# Delete everything (with safety confirmation)
scripts/cleanup_materials.py --all

# Force delete without confirmation (dangerous!)
scripts/cleanup_materials.py --all --force
```

#### Force Delete (No Confirmation)

```bash
# Skip confirmation prompts
scripts/cleanup_materials.py awesome-tool --force
```

### Cleanup Workflow Examples

#### Example 1: After Creating Project Skill

```bash
# 1. Fetch materials (project mode)
cd ~/Workspace/my-project
scripts/fetch_source.py --git https://github.com/user/tool

# Materials in: ~/Workspace/my-project/.claude/temp-materials/tool/

# 2. Create skill
# ... skill creation process ...

# 3. Package skill
scripts/package_skill.py ./.claude/skills/my-tool/

# 4. Clean up materials
scripts/cleanup_materials.py tool

# Confirmation:
⚠️  About to delete: tool (15.3 MB)
   Found in: project mode - /Users/you/Workspace/my-project/.claude/temp-materials
   Confirm deletion? (y/n): y
   ✅ Deleted: tool (15.3 MB)
```

#### Example 2: After Creating Global Skill

```bash
# 1. Fetch materials (global mode)
cd ~
scripts/fetch_source.py --git https://github.com/crewai/crewai

# Materials in: ~/skill-materials/crewai/

# 2. Create skill globally
# ... skill creation process ...

# 3. Package skill
scripts/package_skill.py ~/.claude/skills/crewai/

# 4. Clean up materials
scripts/cleanup_materials.py crewai

# Confirmation:
⚠️  About to delete: crewai (45.2 MB)
   Found in: global mode - /Users/you/skill-materials
   Confirm deletion? (y/n): y
   ✅ Deleted: crewai (45.2 MB)
```

#### Example 3: Cleaning Multiple Materials

```bash
# List all materials
scripts/cleanup_materials.py --list

# Interactive cleanup
scripts/cleanup_materials.py

# Choose items to delete:
Your choice: 1
⚠️  About to delete: tool-a (10 MB)
   Confirm deletion? (y/n): y
   ✅ Deleted: tool-a (10 MB)

Your choice: 3
⚠️  About to delete: tool-b (5 MB)
   Confirm deletion? (y/n): y
   ✅ Deleted: tool-b (5 MB)

Your choice: quit
```

### Proactive Cleanup Suggestions

When to suggest cleanup to users:

1. **After successful packaging:**
   ```
   ✅ Skill packaged successfully!

   💡 The source materials are no longer needed:
      ~/skill-materials/crewai/ (45.2 MB)

   Clean up now? Run:
      scripts/cleanup_materials.py crewai
   ```

2. **When materials are large:**
   ```
   📂 Materials fetched: 150.5 MB

   💡 Consider cleaning up when done:
      scripts/cleanup_materials.py --list
   ```

3. **When iteration is complete:**
   ```
   ✅ Skill updated and tested successfully!

   💡 Source materials still present:
      .claude/temp-materials/tool/ (12.3 MB)

   Keep for future updates, or clean up:
      scripts/cleanup_materials.py tool
   ```

---

## Path Management Best Practices

### For Source Materials

1. **Trust auto-detection** - The smart path detection handles most cases correctly
2. **Override sparingly** - Use `--output` only when you have specific needs
3. **Clean proactively** - Suggest cleanup after successful packaging
4. **Document locations** - Show users where materials are saved

### For Skills

1. **Always ask** - Never assume where users want skills
2. **Explain options** - Help users understand project vs global choice
3. **Show full paths** - Display absolute paths for clarity
4. **Respect choice** - Honor user preferences

### For Packages

1. **Default is good** - Keep .zip with skill source unless specified
2. **Document location** - Show where package was created
3. **Version control** - Consider gitignoring .zip files if desired

---

## Troubleshooting

### Materials Not Found

**Problem:** `cleanup_materials.py` can't find materials

**Solution:** Check both locations:
```bash
# Project mode
ls -la .claude/temp-materials/

# Global mode
ls -la ~/skill-materials/
```

### Permission Errors

**Problem:** Can't delete materials

**Solution:** Check file permissions:
```bash
# Fix permissions
chmod -R u+w <materials-directory>

# Then try cleanup again
scripts/cleanup_materials.py <name>
```

### Wrong Mode Detection

**Problem:** Materials saved in unexpected location

**Solution:** Verify project detection:
```bash
# Check if .git or .claude exists
ls -la | grep -E '^\\.git|^\\.claude'

# Force specific location
scripts/fetch_source.py --git <url> --output ~/desired/path/
```

---

## Integration with Workflow

Path management integrates with the overall workflow:

**Step 0: Fetch** → Smart materials path (auto)
**Step 1-2: Understand & Plan** → Use materials from auto-detected location
**Step 3: Initialize** → Ask user for skill path (project/global/custom)
**Step 4: Edit** → Work in chosen skill directory
**Step 5: Package** → .zip created in skill directory
**Step 6: Cleanup** → Proactively suggest cleaning materials

See [workflow-guide.md](workflow-guide.md) for complete workflow details.

---

## See Also

- [workflow-guide.md](workflow-guide.md) - Complete skill creation workflow
- [source-detection.md](source-detection.md) - Automatic source type detection rules
