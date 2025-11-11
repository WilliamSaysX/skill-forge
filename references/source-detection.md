# Source Detection Rules - Detailed Guide

Automatic detection of source material types and how to handle each.

## Overview

When users provide a source for skill creation, automatically detect the type and handle it appropriately:

| Source Type | Detection Pattern | Action | Tool Used |
|-------------|------------------|---------|-----------|
| **GitHub Repository** | `github.com` in URL | Clone repository | `fetch_source.py --git` |
| **Online Documentation** | Documentation site URL | Scrape documentation | `fetch_source.py --docs` |
| **Local Directory** | File path exists locally | Use directly | No fetching needed |
| **Ambiguous** | Unclear or mixed | Ask user for clarification | Manual decision |

---

## Detection Rules

### Rule 1: GitHub Repository URLs

**Pattern Matching:**

```python
# Detect GitHub URLs
patterns = [
    r'github\.com/[\w-]+/[\w-]+',           # https://github.com/user/repo
    r'https?://github\.com/[\w-]+/[\w-]+',  # With protocol
    r'git@github\.com:[\w-]+/[\w-]+\.git',  # SSH format
]
```

**Examples:**

✅ **Recognized:**
- `https://github.com/joaomdmoura/crewAI`
- `github.com/user/awesome-tool`
- `git@github.com:user/repo.git`
- `https://github.com/anthropics/anthropic-sdk-python`

❌ **Not GitHub:**
- `https://gitlab.com/user/repo` (different platform)
- `https://docs.crewai.com` (documentation site)
- `~/local/repo/` (local path)

**Action:**

```bash
# Automatically execute (no asking):
scripts/fetch_source.py --git <github-url>
```

**Proactive Behavior:**

```
User: "Create a skill from https://github.com/joaomdmoura/crewAI"

Claude: I'll fetch the crewAI repository and create a skill from it.

[Executes immediately:]
scripts/fetch_source.py --git https://github.com/joaomdmoura/crewAI

[After fetching:]
✅ Repository cloned successfully
📂 Materials ready at: <auto-detected-path>/crewAI/
```

### Rule 2: Online Documentation URLs

**Pattern Matching:**

```python
# Detect documentation sites
doc_indicators = [
    'docs.',              # docs.example.com
    '/docs/',             # example.com/docs/
    '/documentation/',    # example.com/documentation/
    'readthedocs.io',     # project.readthedocs.io
    '/guide/',            # example.com/guide/
    '/api/',              # example.com/api/
]
```

**Examples:**

✅ **Recognized:**
- `https://docs.crewai.com`
- `https://python.langchain.com/docs/`
- `https://fastapi.tiangolo.com/`
- `https://project.readthedocs.io/en/latest/`
- `https://example.com/documentation/getting-started`

❌ **Not Documentation:**
- `https://github.com/user/repo` (GitHub repo)
- `~/docs/local-files/` (local path)
- `https://example.com/blog/` (blog, not docs)

**Action:**

```bash
# Extract name from URL and execute:
scripts/fetch_source.py --docs <docs-url> --name <project-name>
```

**Name Extraction Logic:**

```python
# Extract meaningful name from URL
https://docs.crewai.com → crewai
https://fastapi.tiangolo.com → fastapi
https://python.langchain.com/docs/ → langchain
```

**Proactive Behavior:**

```
User: "Create a skill from https://docs.crewai.com"

Claude: I'll scrape the crewAI documentation and create a skill from it.

[Executes immediately:]
scripts/fetch_source.py --docs https://docs.crewai.com --name crewai

[After scraping:]
✅ Documentation scraped successfully
📂 Materials ready at: <auto-detected-path>/crewai/
```

### Rule 3: Local Directory Paths

**Pattern Matching:**

```python
# Detect local paths
path_indicators = [
    starts_with('~/'),           # Home directory
    starts_with('/'),            # Absolute path
    starts_with('./'),           # Relative path
    starts_with('../'),          # Parent directory
    os.path.exists(path),        # Actually exists
]
```

**Examples:**

✅ **Recognized:**
- `~/projects/my-tool/`
- `/Users/username/Documents/tool/`
- `./local-directory/`
- `../sibling-project/`

❌ **Not Local Path:**
- `https://github.com/user/repo` (URL)
- `https://docs.example.com` (URL)

**Action:**

No fetching needed! Use the directory directly.

**Proactive Behavior:**

```
User: "Create a skill from ~/projects/awesome-tool/"

Claude: I'll create a skill from your local directory.

[No fetching - uses directory directly]

✅ Using local directory: /Users/you/projects/awesome-tool/
📂 Analyzing contents...
```

### Rule 4: Ambiguous or Mixed Sources

**When to Ask:**

1. **Unclear source type:**
   - User says "create a skill for X" without providing a source
   - Provided text doesn't match any pattern
   - Multiple possible interpretations

2. **Complex requests:**
   - Wants both repo AND docs
   - Multiple sources specified
   - Custom requirements

**Examples:**

❓ **Ambiguous:**
- `"Create a skill for FastAPI"` (no source specified)
- `"crewai"` (name only, could be many things)
- `"the tool I mentioned earlier"` (context-dependent)

**Asking Behavior:**

```
User: "Create a skill for FastAPI"

Claude: I can help create a FastAPI skill. Where should I get the source materials?

1. Clone the GitHub repository (https://github.com/tiangolo/fastapi)
2. Scrape the documentation (https://fastapi.tiangolo.com)
3. Use a local directory you already have
4. Both repository and documentation

Which would you prefer?
```

---

## Detection Decision Tree

```
User provides source
│
├─── Matches GitHub URL pattern?
│    ├─ YES → Execute fetch_source.py --git <url>
│    └─ NO → Continue
│
├─── Matches documentation URL pattern?
│    ├─ YES → Execute fetch_source.py --docs <url> --name <extracted-name>
│    └─ NO → Continue
│
├─── Matches local path pattern AND exists?
│    ├─ YES → Use directory directly (no fetch)
│    └─ NO → Continue
│
└─── Ambiguous or unclear
     └─ Ask user for clarification
```

---

## Comprehensive Examples

### Example 1: GitHub Repository

**User Input:**
```
"Create a skill from https://github.com/joaomdmoura/crewAI"
```

**Detection:**
- ✅ Contains `github.com`
- ✅ Valid GitHub URL pattern
- Result: **GitHub Repository**

**Action:**
```bash
# Detect project root for smart path
# Execute immediately:
scripts/fetch_source.py --git https://github.com/joaomdmoura/crewAI

# Output:
📍 Project mode detected
   Project root: /Users/you/Workspace/current-project
   Materials will be saved in project: .claude/temp-materials/

CLONING REPOSITORY
==================
URL: https://github.com/joaomdmoura/crewAI
Output: /Users/you/Workspace/current-project/.claude/temp-materials/crewAI

✅ Clone successful
```

### Example 2: Online Documentation

**User Input:**
```
"Create a skill from https://docs.crewai.com"
```

**Detection:**
- ✅ Contains `docs.`
- ✅ Documentation URL pattern
- Extract name: `crewai`
- Result: **Online Documentation**

**Action:**
```bash
# Execute immediately:
scripts/fetch_source.py --docs https://docs.crewai.com --name crewai

# Output:
📍 Global mode
   Materials will be saved in: ~/skill-materials/

SCRAPING DOCUMENTATION
======================
URL: https://docs.crewai.com
Name: crewai

📥 Running doc_scraper.py...
✅ Documentation scraped successfully
```

### Example 3: Local Directory

**User Input:**
```
"Create a skill from ~/projects/my-awesome-tool/"
```

**Detection:**
- ✅ Starts with `~/`
- ✅ Path exists on filesystem
- Result: **Local Directory**

**Action:**
```bash
# No fetching needed
# Use directory directly

# Response:
✅ Using local directory: /Users/you/projects/my-awesome-tool/
📂 Analyzing contents...

Directory contains:
- Python files: 45
- Markdown files: 12
- JSON files: 3
Total size: 2.3 MB

Proceeding to Step 1: Understanding the skill requirements...
```

### Example 4: GitHub + Documentation (Combined)

**User Input:**
```
"Create a skill from the crewAI repo and docs"
```

**Detection:**
- Mentions both repo and docs
- Ambiguous - need clarification
- Result: **Ask User**

**Action:**
```
I can fetch both the crewAI repository and documentation. Here are the options:

1. Repository only: https://github.com/joaomdmoura/crewAI
2. Documentation only: https://docs.crewai.com
3. Both (repository + documentation)

Which would you prefer?
```

**If user chooses "Both":**
```bash
# Execute combined fetch:
scripts/fetch_source.py \
  --git https://github.com/joaomdmoura/crewAI \
  --docs https://docs.crewai.com \
  --name crewai

# Result:
# Materials in: <auto-detected-path>/crewai/
# ├── [repository contents]
# └── docs_scraped/
#     └── [scraped documentation]
```

### Example 5: Ambiguous Name Only

**User Input:**
```
"Create a skill for Anthropic SDK"
```

**Detection:**
- No URL provided
- No path provided
- Just a name/description
- Result: **Ask User**

**Action:**
```
I can help create an Anthropic SDK skill. Where should I get the source materials?

I found these possible sources:
1. GitHub repository: https://github.com/anthropics/anthropic-sdk-python
2. Documentation: https://docs.anthropic.com/
3. Both repository and documentation
4. You have a local directory with the materials

Which would you like to use?
```

---

## Special Cases

### GitLab, Bitbucket, and Other Git Platforms

**Current Status:** Not auto-detected (only GitHub is)

**Reason:** Different platforms have different access patterns and authentication

**Handling:**

```
User: "Create a skill from https://gitlab.com/user/project"

Claude: I notice you're using GitLab. I can help fetch this repository.

Would you like me to:
1. Clone it using git (you'll need access configured)
2. You fetch it manually and provide the local path

For option 1, I'll run:
git clone https://gitlab.com/user/project

Which would you prefer?
```

### Private Repositories

**Detection:** Can't determine if repo is private from URL alone

**Handling:**

```bash
# Attempt clone, let it fail naturally if auth needed
scripts/fetch_source.py --git https://github.com/user/private-repo

# If fails:
❌ Clone failed: Authentication required

Claude suggests:
This appears to be a private repository. You can:
1. Configure git credentials (SSH key or token)
2. Clone manually: git clone https://github.com/user/private-repo ~/materials/repo
3. Use a local directory you already have access to
```

### Documentation Behind Authentication

**Detection:** Can't detect auth requirements from URL

**Handling:**

```bash
# Attempt scrape, may fail if auth required
scripts/fetch_source.py --docs https://internal-docs.company.com --name internal

# If fails:
❌ Documentation scraping failed: 403 Forbidden

Claude suggests:
This documentation requires authentication. You can:
1. Provide API credentials if doc_scraper.py supports them
2. Download the docs manually and provide the local path
3. Use publicly accessible documentation if available
```

### Monorepos and Subdirectories

**User Wants Specific Subdirectory:**

```
User: "Create a skill from the Python SDK in https://github.com/anthropics/anthropic-sdk-python"

Claude: I'll clone the repository and focus on the Python SDK portion.

[Clones full repo]

📂 Repository cloned
📁 Focusing on Python SDK directory for skill creation...
```

**After Cloning:**
- Use only relevant subdirectory for analysis
- May suggest cleaning up unneeded parts

---

## Name Extraction Logic

### From GitHub URLs

```python
def extract_github_name(url):
    # https://github.com/joaomdmoura/crewAI → crewAI
    # https://github.com/anthropics/anthropic-sdk-python → anthropic-sdk-python

    parts = url.rstrip('/').rstrip('.git').split('/')
    return parts[-1]
```

**Examples:**
- `https://github.com/user/awesome-tool` → `awesome-tool`
- `https://github.com/org/my-project.git` → `my-project`

### From Documentation URLs

```python
def extract_docs_name(url):
    # https://docs.crewai.com → crewai
    # https://fastapi.tiangolo.com → fastapi
    # https://python.langchain.com/docs/ → langchain

    domain = urlparse(url).netloc

    # Remove common prefixes
    if domain.startswith('docs.'):
        return domain[5:].split('.')[0]  # docs.example.com → example

    # Use main domain name
    return domain.split('.')[0]  # example.com → example
```

**Examples:**
- `https://docs.crewai.com` → `crewai`
- `https://fastapi.tiangolo.com` → `fastapi`
- `https://python.langchain.com/docs/` → `langchain`

### From Local Paths

```python
def extract_local_name(path):
    # ~/projects/awesome-tool/ → awesome-tool
    # /Users/me/tool-name/ → tool-name

    return Path(path).name
```

**Examples:**
- `~/projects/my-tool/` → `my-tool`
- `/Users/me/awesome-project/` → `awesome-project`

---

## Override Detection

### Manual Source Specification

Users can always override auto-detection:

```
User: "Fetch https://example.com as documentation even though it doesn't match the pattern"

Claude: I'll fetch it as documentation using:
scripts/fetch_source.py --docs https://example.com --name example
```

### Multiple Sources

```
User: "Get both the repo and docs for crewAI"

Claude: I'll fetch both:
scripts/fetch_source.py \
  --git https://github.com/joaomdmoura/crewAI \
  --docs https://docs.crewai.com \
  --name crewai
```

### Custom Options

```
User: "Clone the repo but use shallow clone"

Claude: I'll use shallow clone for faster fetching:
scripts/fetch_source.py \
  --git https://github.com/user/repo \
  --depth 1
```

---

## Error Handling

### Invalid URL

```
User: "Create skill from htp://broken-url"

Claude: The URL appears invalid. Could you verify:
- GitHub repository URL (e.g., https://github.com/user/repo)
- Documentation URL (e.g., https://docs.example.com)
- Local directory path (e.g., ~/projects/tool/)
```

### Nonexistent Local Path

```
User: "Create skill from ~/nonexistent/path/"

Claude: The path ~/nonexistent/path/ doesn't exist.

Would you like to:
1. Provide a different local path
2. Fetch from a GitHub repository instead
3. Fetch from online documentation instead
```

### Network Errors

```
# fetch_source.py fails
❌ Clone failed: Network error

Claude: The fetch failed due to network issues.

You can:
1. Try again: scripts/fetch_source.py --git <url>
2. Use a local directory if you already have the materials
3. Check your internet connection
```

---

## Best Practices

### 1. Proactive Detection

Always try to detect and act immediately for clear cases:

```
✅ GOOD:
User: "https://github.com/user/repo"
Claude: [Immediately clones without asking]

❌ BAD:
User: "https://github.com/user/repo"
Claude: "Do you want me to clone this?" [Unnecessary question]
```

### 2. Ask When Ambiguous

Don't guess for unclear requests:

```
✅ GOOD:
User: "Create a skill for FastAPI"
Claude: "Where should I get the materials? [Lists options]"

❌ BAD:
User: "Create a skill for FastAPI"
Claude: [Guesses and clones wrong repo]
```

### 3. Show What You're Doing

Always communicate the action being taken:

```
✅ GOOD:
"I'll fetch the crewAI repository and create a skill from it."
[Shows fetch_source.py command]

❌ BAD:
[Silently executes without explanation]
```

### 4. Handle Failures Gracefully

Provide helpful next steps when things fail:

```
✅ GOOD:
"Clone failed: Authentication required.
You can: [concrete options]"

❌ BAD:
"Error occurred."
```

---

## Integration with Workflow

Source detection happens at **Step 0** of the workflow:

**Step 0: Fetch Source Materials (Automatic)**
1. Detect source type (GitHub/Docs/Local)
2. Execute appropriate fetch command
3. Use smart path selection
4. Confirm materials are ready

**Then proceed to:**
- Step 1: Understanding the skill
- Step 2: Planning contents
- ... (see workflow-guide.md)

---

## See Also

- [workflow-guide.md](workflow-guide.md) - Complete skill creation workflow
- [path-management.md](path-management.md) - Path management and cleanup strategies
