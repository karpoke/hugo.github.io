# GitHub Copilot Instructions

This document contains guidelines and context for GitHub Copilot to efficiently assist in this blog's development.

## 📋 Project Context

### Technologies
- **Framework**: Hugo (Static Site Generator)
- **Hugo Version**: 0.156.0 (extended)
- **Theme**: PaperMod (git submodule)
- **Deploy**: GitHub Pages with GitHub Actions
- **Language**: Markdown for content, TOML for configuration
- **Site Title**: Karpoke - Just Another Hugo Blog
- **Domain**: hugo.github.io (temporary), blog.ignaciocano.com (final)

### Blog Structure
```
hugo.github.io/
├── content/posts/          # Blog articles
├── static/                 # Static files (CNAME, images, etc.)
├── themes/PaperMod/        # Theme (submodule)
├── .github/workflows/      # CI/CD
├── hugo.toml              # Main configuration
└── Makefile               # Useful commands
```

## 🎯 Project Goals

1. **Technical blog**: Content about programming, DevOps, databases, web development
2. **Critical SEO**: Maintain Pelican legacy URLs (`/YYYY/MM/DD/slug/`)
3. **Search**: Integrated with Fuse.js on the frontend
4. **Automatic deploy**: Push to `main` → GitHub Actions → GitHub Pages

## 🔧 Code Conventions

### Language in Code
All generated code **must be in English**: templates, CSS, JavaScript, comments, variable names, function names, and documentation. Spanish is only used for blog post content.



### Post Format
All articles must follow this frontmatter:

```markdown
---
title: "Post Title"
date: YYYY-MM-DDTHH:MM:SS+01:00
tags: ["tag1", "tag2", "tag3"]
slug: url-friendly-post-slug
description: "Brief description for SEO"
categories: ["category"]
---

## Content here...
```

### Common Commands
- `make server` - Local development server
- `make build` - Generate static site
- `make new-post TITLE="Title"` - Create new post
- `make new-micropost URL="https://..."` - Create micropost from URL
- `make clean` - Clean generated files

### Legacy URLs (CRITICAL)
URLs MUST maintain this exact format for SEO:
```
/YYYY/MM/DD/slug/
```

Configured in `hugo.toml`:
```toml
[permalinks]
  posts = '/:year/:month/:day/:slug/'
```

## 📝 When Creating Content

### Blog Posts
- **Language**: Spanish
- **Tone**: Technical but accessible
- **Code**: Include practical examples with syntax highlighting
- **SEO**: Always include `description` in frontmatter
- **Tags**: Use consistent, relevant tags
- **Categories**: Post must have its directory name as a category (e.g., posts in `content/posts/admin/` must have `categories: ["admin"]`)

### Code Examples
Use code blocks with the language specified:

````markdown
```python
def example():
    return "Code with syntax highlighting"
```
````

### Images
Place in `static/images/` and reference as:
```markdown
![Description](/images/image-name.png)
```

## 🚫 Restrictions and Precautions

### DO NOT include:
- ❌ Real credentials (passwords, tokens, API keys)
- ❌ Local system paths (`/home/user/...`)
- ❌ Sensitive personal information
- ❌ SSH keys or certificates

### DO NOT modify without confirming:
- ⚠️ Permalink format (legacy URLs)
- ⚠️ GitHub Actions configuration
- ⚠️ PaperMod theme submodule

### Always verify:
- ✅ Date format in frontmatter (ISO 8601)
- ✅ `slug` field present in each post
- ✅ Tags in quotes and as array
- ✅ Correct categories for post location

## 🔍 Search and Navigation

### Search Configuration
The site uses Fuse.js for frontend search:
- Special file: `content/search.md`
- JSON output configured in `hugo.toml`
- Index at: `public/index.json`

### Main Menu
Configured in `hugo.toml` under `[menu.main]`:
- Posts
- Tags
- Search

## 🛠️ Common Tasks

### Create a new post
```bash
\make new-post TITLE="My Post"
# Edit: content/posts/my-post.md
# Verify: make server
# Commit and push
```

### Create a micropost from URL
```bash
\make new-micropost URL="https://example.com/article"
# Or with draft flag
\make new-micropost URL="https://example.com" DRAFT=1
```

### Update PaperMod theme
```bash
\make update-theme
# Verify changes
\git commit -am "Update PaperMod theme"
\git push
```

### Debugging
```bash
# View build errors
\hugo --verbose

# Clean and rebuild
\make clean && \make build

# View GitHub Actions logs
# Go to: https://github.com/karpoke/hugo.github.io/actions
```

## 📦 Deploy

### Automatic Process
1. Push to `main` branch
2. GitHub Actions runs workflow
3. Hugo generates static site
4. Deploy to GitHub Pages
5. Site updated in ~1-2 minutes

### Workflow
- File: `.github/workflows/hugo.yml`
- Hugo version: 0.156.0
- Includes: Dart Sass, optimizations, minify

## 🎨 Theme Customization

### PaperMod Configuration
In `hugo.toml` under `[params]`:
- Search enabled with Fuse.js
- Share buttons in posts (X/Twitter, LinkedIn, Reddit, Facebook, WhatsApp, Telegram, HackerNews)
- Code with copy button
- TOC (table of contents)
- Reading time estimate
- Breadcrumbs
- GitHub social icon in header pointing to `https://github.com/karpoke/`

### Overrides
To customize the theme, create files in:
- `layouts/` - For templates
- `assets/` - For custom CSS/JS
- `static/` - For static files

## 📐 LaTeX and Mathematical Equations

### Enabling Math Support
The blog uses **MathJax 3** to render LaTeX equations. It's configured via:
- `hugo.toml`: `params.math = true` (global) or per-post via frontmatter
- `layouts/partials/math.html`: MathJax script loader
- `assets/css/math.css`: Custom styling for equations

### Using LaTeX in Posts

**In frontmatter** (to enable for specific post):
```yaml
---
title: "My Post"
math: true
---
```

**Display equations** (centered, on own line):
```markdown
$$
\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

**Inline equations**:
```markdown
The quadratic formula is $\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$ for equation $ax^2 + bx + c = 0$.
```

**Complex expressions** (using align environment):
```markdown
$$
\begin{align*}
ax^2 + bx + c &= 0 \\
x &= \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
\end{align*}
$$
```

### MathJax Delimiters
- **Display math**: `$$...$$` or `\[...\]`
- **Inline math**: `$...$` or `\(...\)`
- **LaTeX environments**: `\begin{align*}...\end{align*}`, `\begin{equation}...\end{equation}`, etc.

### Example Post
See `content/posts/2011/03/latex-en-wordpress.md` for a complete example with quadratic formula.

## 📚 Resources

### Documentation
- [Hugo Docs](https://gohugo.io/documentation/)
- [PaperMod Wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)
- [Hugo Permalinks](https://gohugo.io/content-management/urls/)

### Useful Hugo Commands
```bash
\hugo --help
\hugo server --help
\hugo new --help
\hugo config
```

## 🧪 Testing

### Local
```bash
# Server with drafts
\make server

# Production build
\make build

# Check for broken links
\hugo --printPathWarnings
```

### Pre-Deploy Checklist
- [ ] ✅ Internal links work
- [ ] ✅ Images load correctly
- [ ] ✅ URLs follow legacy format
- [ ] ✅ Search works
- [ ] ✅ No errors in `hugo --verbose`
- [ ] ✅ Correct tags
- [ ] ✅ Date in ISO format

## ⚙️ Git Configuration

### Pager Disabled
The project is configured to NOT use pager in git (useful for scripting and CI/CD):

```bash
# Configuration applied in .git/config:
core.pager = cat
pager.branch = false
pager.log = false
pager.diff = false
```

This means commands like `git log`, `git diff`, `git branch` will show output directly without using `less` or similar.

### Custom SSH
The repository uses a specific SSH key:
```bash
core.sshCommand = ssh -i /home/hbxuser/karpoke/ssh/id_rsa -o IdentitiesOnly=yes
```

**Note**: This configuration is local and not uploaded to the repository.

### Git Hooks
The project includes a pre-commit hook that validates Hugo builds:

```bash
# Install hooks
\make install-hooks

# Hook location
.git/hooks/pre-commit  # Active hook (not in repo)
scripts/pre-commit     # Source script (in repo)
```

**What the pre-commit hook does:**
- ✅ Validates Hugo can generate the site without errors
- ✅ Runs `hugo --quiet --minify`
- ✅ Cleans up auto-generated files
- ✅ Prevents commits with syntax errors

**Skip the hook (emergencies only):**
```bash
\git commit --no-verify -m "message"
```

## 🎯 Automation Rules

### Bash Command Escaping
Always prefix bash commands with `\` to prevent alias expansion:

```bash
\git status
\grep -r "foo" .
\python3 script.py
```

This ensures the real binary is called, not a user-defined alias.

### Terminal Output Verification
When executing commands or scripts, ensure they return output (even in cases where they shouldn't return anything, like when no files are found).

If a command would normally return no output, add output verification:

```bash
command && echo "ok" || echo "ko"
```

**Why**: This helps identify if the terminal is hanging, unresponsive, or if the command succeeded/failed silently.

**If the terminal returns no output**:
- Do NOT assume success
- Repeat the command in a new terminal
- Add output verification (the `&& echo "ok" || echo "ko"` pattern)
- If still no output, try breaking the command into smaller parts

### Commands Without Confirmation
The following commands do NOT require prior confirmation, even if chained with `&&`:
- `cd` - Change directory
- `git add` - Stage files
- `git diff` - View file differences
- `git log` - View commit history
- `git status` - View repository status
- `git check-ignore` - Check if files are ignored
- `git show` - Show commits
- `git reflog` - View reference history

Examples that do NOT require confirmation:
```bash
\cd /path && \git add file.txt
\git diff file.txt
\git status
```

### Commands Requiring Explicit User Authorization
- `git commit` - Do NOT commit until user explicitly asks
- `git push` - NEVER push without explicit user confirmation
- `git push --force` - Dangerous command, requires confirmation
- `git reset --hard` - Destructive command, requires confirmation
- `git rebase` - Command that rewrites history
- `git force-push` - Variant of push --force

**⛔ CRITICAL RULE**: NEVER execute `git commit` proactively, even if changes are staged and ready. ALWAYS wait for the user to explicitly say "commit", "make a commit" or similar. This applies even at the end of a completed task.

### Automatic Instruction Updates
When new rules or conventions are discovered during work:
- Update this file automatically
- Include in the same commit where the rule applies
- Document the change in the appropriate section

## 🔐 Security

### Sensitive Information
**NEVER include in code/commits**:
- Real passwords
- API tokens
- Private SSH keys
- Environment variables with secrets

### Code Examples
Examples in articles **CAN** include:
- Example passwords (`dev_password_123`)
- Example URLs (`example.com`)
- Fictitious data for tutorials

### .gitignore
Verify it includes:
- `public/`
- `resources/`
- `.env`
- `*.log`
- IDE files (`.idea/`, `.vscode/`)

## 💡 Suggestions for Copilot

### When generating blog content:
1. Use clear technical Spanish
2. Include real code examples
3. Add tables when useful
4. Use emojis sparingly (only in titles)
5. Create lists for better readability

### When modifying configuration:
1. Comment important changes
2. Keep TOML format clean
3. Document new features
4. Verify PaperMod compatibility

### When creating Make commands:
1. Add help comments (`## description`)
2. Use `.PHONY` for targets
3. Handle errors appropriately

## 🎓 Project Patterns

### Naming Conventions
- **Files**: kebab-case (`my-post.md`)
- **Slugs**: kebab-case without accents (`optimizing-sql-queries`)
- **Tags**: lowercase, Spanish (`python`, `databases`)
- **Git branches**: kebab-case (`feature/new-feature`)

### Commits
Use semantic commit messages following the format: `type(scope): description`

**Format rules (important):**
- **The first line (title) must be maximum 50 characters.**
- Body is **optional** and only included when title is insufficient:
  - Different things changed that deserve individual explanation
  - Change reason is not obvious and adds relevant context
  - If title is clear and complete, **do not add body**
- When using body, separate from title with **one blank line**
- **Each body line must be maximum 72 characters.**

Example:
```
feat(hugo): add archives page using PaperMod layout

- Create content/archivo.md with layout: archives
- Add Archivo entry to main menu in hugo.toml
```

**Allowed commit types:**
- `feat:` - New functionality
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Format changes (spaces, quotes, etc.) without affecting code
- `refactor:` - Code refactoring without changing functionality
- `perf:` - Performance improvements
- `test:` - Add or modify tests
- `chore:` - Build tools, dependencies, etc.
- `ci:` - CI/CD configuration changes

**Scope (optional but recommended):**
- `hugo` - Hugo configuration
- `post` - Blog articles
- `theme` - PaperMod theme changes
- `hooks` - Git hooks
- `workflow` - GitHub Actions

**Correct examples:**
```
feat(post): add new article about Docker Compose
fix(hugo): correct date format in frontmatter
docs(copilot-instructions): clarify semantic commit rules
feat(theme): add custom CSS for syntax highlighting
chore(deps): update PaperMod to latest version
ci(workflow): update Hugo version to 0.156.0
```

**Full format:**
```
type(scope): description

[optional body - additional details if necessary]

[optional footer - issue references, breaking changes, etc.]
```


---

**Last update**: February 2026  
**Maintainer**: Nacho Cano (@karpoke)  
**Repository**: https://github.com/karpoke/hugo.github.io

