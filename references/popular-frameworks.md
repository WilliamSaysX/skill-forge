# Popular Frameworks & Libraries Source Guide

This reference provides quick access to documentation URLs and source information for popular frameworks and libraries. Use this when creating skills for well-known technologies.

## Quick Reference Table

| Framework | llms.txt | Docs URL | GitHub |
|-----------|----------|----------|--------|
| **React** | ❌ | https://react.dev/ | facebook/react |
| **Vue** | ✅ | https://vuejs.org/ | vuejs/core |
| **Svelte** | ✅ | https://svelte.dev/ | sveltejs/svelte |
| **Next.js** | ❌ | https://nextjs.org/ | vercel/next.js |
| **FastAPI** | ❌ | https://fastapi.tiangolo.com/ | tiangolo/fastapi |
| **Django** | ❌ | https://docs.djangoproject.com/ | django/django |
| **Flask** | ❌ | https://flask.palletsprojects.com/ | pallets/flask |
| **Tailwind CSS** | ❌ | https://tailwindcss.com/ | tailwindlabs/tailwindcss |

---

## Frontend Frameworks

### React
```
Documentation: https://react.dev/
llms.txt: ❌ Not available
GitHub: https://github.com/facebook/react
Language: JavaScript/TypeScript

Recommended categories:
- getting_started: Quick start, installation
- components: Component basics, props, JSX
- hooks: useState, useEffect, useContext, custom hooks
- state: State management, context
- api_reference: API documentation
- examples: Code examples and patterns
```

**Usage:**
```bash
python scripts/fetch_source.py --git https://github.com/facebook/react --depth 1
python scripts/fetch_source.py --docs https://react.dev/ --name react
```

---

### Vue
```
Documentation: https://vuejs.org/
llms.txt: ✅ https://vuejs.org/llms-full.txt
GitHub: https://github.com/vuejs/core
Language: JavaScript/TypeScript

Recommended categories:
- essentials: Introduction, creating an application
- components: Component basics, props, events
- reactivity: Reactivity fundamentals, computed, watchers
- composition: Composition API, lifecycle
- built_ins: Directives, components, special attributes
- scaling_up: Routing, state management, testing
```

**Usage (with llms.txt - faster):**
```bash
python scripts/detect_llms_txt.py https://vuejs.org/
python scripts/fetch_source.py --docs https://vuejs.org/llms-full.txt --name vue
```

**Usage (full scrape):**
```bash
python scripts/fetch_source.py --docs https://vuejs.org/ --name vue
```

---

### Svelte
```
Documentation: https://svelte.dev/
llms.txt: ✅ https://svelte.dev/llms.txt
GitHub: https://github.com/sveltejs/svelte
Language: JavaScript/TypeScript

Recommended categories:
- introduction: Getting started, tutorial
- components: Basics, logic, events, bindings
- reactivity: Declarations, statements, stores
- advanced: Context, special elements, module context
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://svelte.dev/llms.txt --name svelte
```

---

### Next.js
```
Documentation: https://nextjs.org/
llms.txt: ❌ Not available
GitHub: https://github.com/vercel/next.js
Language: JavaScript/TypeScript

Recommended categories:
- getting_started: Installation, project structure
- routing: Pages, dynamic routes, API routes
- data_fetching: getStaticProps, getServerSideProps
- deployment: Build, optimization, deployment
- api: API reference
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://nextjs.org/docs --name nextjs
python scripts/fetch_source.py --git https://github.com/vercel/next.js --depth 1
```

---

## Backend Frameworks

### FastAPI
```
Documentation: https://fastapi.tiangolo.com/
llms.txt: ❌ Not available
GitHub: https://github.com/tiangolo/fastapi
Language: Python

Recommended categories:
- tutorial: First steps, path parameters, query parameters
- path_operations: Request body, response model, forms
- dependencies: Dependency injection, security
- security: OAuth2, JWT, API keys
- database: SQL databases, async databases
- advanced: Middleware, testing, async
- deployment: Docker, servers, HTTPS
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://fastapi.tiangolo.com/ --name fastapi
python scripts/fetch_source.py --git https://github.com/tiangolo/fastapi --depth 1
```

**Multi-source (docs + code):**
```bash
# Fetch both sources
python scripts/fetch_source.py --git https://github.com/tiangolo/fastapi --depth 1 --name fastapi
python scripts/fetch_source.py --docs https://fastapi.tiangolo.com/ --name fastapi --output ~/.claude/temp-materials/fastapi/docs

# Then create skill from both
# Claude will help organize both sources
```

---

### Django
```
Documentation: https://docs.djangoproject.com/
llms.txt: ❌ Not available
GitHub: https://github.com/django/django
Language: Python

Recommended categories:
- getting_started: Installation, tutorial
- models: Database models, queries, migrations
- views: URL dispatcher, views, templates
- forms: Form handling, validation
- admin: Admin site customization
- security: Authentication, permissions, CSRF
- deployment: Deployment checklist, servers
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://docs.djangoproject.com/en/stable/ --name django
```

---

### Flask
```
Documentation: https://flask.palletsprojects.com/
llms.txt: ❌ Not available
GitHub: https://github.com/pallets/flask
Language: Python

Recommended categories:
- quickstart: Installation, minimal application
- tutorial: Application factory, blueprints, templates
- patterns: Application structure, deployment
- api: API reference, configuration
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://flask.palletsprojects.com/ --name flask
```

---

## CSS Frameworks

### Tailwind CSS
```
Documentation: https://tailwindcss.com/
llms.txt: ❌ Not available
GitHub: https://github.com/tailwindlabs/tailwindcss
Language: CSS/PostCSS

Recommended categories:
- getting_started: Installation, editor setup
- core_concepts: Utility-first, responsive, hover/focus
- customization: Configuration, theme, plugins
- utilities: Layout, flexbox, spacing, typography, colors
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://tailwindcss.com/docs --name tailwindcss
```

---

## AI & Machine Learning

### LangChain
```
Documentation: https://python.langchain.com/
llms.txt: ❌ Not available
GitHub: https://github.com/langchain-ai/langchain
Language: Python

Recommended categories:
- get_started: Introduction, installation, quickstart
- modules: Models, prompts, chains, agents
- use_cases: Chatbots, QA, summarization
- integrations: LLM providers, vector stores
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://python.langchain.com/docs/get_started --name langchain
```

---

### CrewAI
```
Documentation: https://docs.crewai.com/
llms.txt: ❌ Not available
GitHub: https://github.com/joaomdmoura/crewAI
Language: Python

Recommended categories:
- core_concepts: Agents, tasks, crews, tools
- how_to: Creating agents, defining tasks, collaboration
- examples: Use cases and patterns
```

**Usage:**
```bash
python scripts/fetch_source.py --git https://github.com/joaomdmoura/crewAI --depth 1
python scripts/fetch_source.py --docs https://docs.crewai.com/ --name crewai
```

---

## Game Development

### Godot
```
Documentation: https://docs.godotengine.org/
llms.txt: ❌ Not available
GitHub: https://github.com/godotengine/godot
Language: GDScript, C++

Recommended categories:
- getting_started: Introduction, first 2D/3D game
- manual: Scenes, nodes, scripting, physics
- scripting: GDScript basics, classes, signals
- tutorials: Step-by-step guides
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://docs.godotengine.org/en/stable/ --name godot
```

---

## Developer Tools

### Vite
```
Documentation: https://vitejs.dev/
llms.txt: ❌ Not available
GitHub: https://github.com/vitejs/vite
Language: JavaScript/TypeScript

Recommended categories:
- guide: Getting started, features, plugins
- config: Configuration reference
- api: Plugin API, JavaScript API
```

**Usage:**
```bash
python scripts/fetch_source.py --docs https://vitejs.dev/guide/ --name vite
```

---

## Tips for Using This Reference

### Detecting llms.txt

Always check for llms.txt first - it's 10x faster:

```bash
python scripts/detect_llms_txt.py <docs-url>
```

If found, use the llms.txt URL directly in fetch_source.py.

### Multi-Source Skills

For comprehensive skills, combine documentation + GitHub:

1. Fetch documentation (for official guides)
2. Fetch GitHub repo (for code examples, issues, changelog)
3. Create skill from both sources
4. Organize into categories

### Custom Frameworks

For frameworks not listed here:

1. Find official documentation URL
2. Check for GitHub repository
3. Run llms.txt detection
4. Analyze doc structure to determine categories
5. Follow the same workflow

### Updating This List

When you discover a new framework or find that a framework now supports llms.txt, update this file to keep it current.

---

**Last Updated:** 2025-01-11
**Frameworks Listed:** 13
**With llms.txt Support:** 2 (Vue, Svelte)
