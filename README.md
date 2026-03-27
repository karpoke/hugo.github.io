# Nacho Cano's Blog

Technical blog built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

Migrated from Pelican while preserving legacy URLs for SEO compatibility.

## 🚀 Local Development

### Requirements
- Hugo (extended version)
- Git
- Make (optional, for simplified commands)

### Clone the repository

```bash
git clone https://github.com/karpoke/hugo.github.io.git
cd hugo.github.io
git submodule update --init --recursive
make install-hooks  # Install git hooks (recommended)
```

### Run local server

With Make:
```bash
make server
```

Without Make:
```bash
hugo server -D
```

The site will be available at `http://localhost:1313`

## 📝 Create a new post

With Make:
```bash
make new-post TITLE="My New Post"
```

Without Make:
```bash
hugo new posts/my-new-post.md
```

## 🏗️ Build

```bash
make build
# or
hugo --minify
```

The generated site will be in `./public/`

## 📦 Deploy

Deploy to GitHub Pages happens automatically via GitHub Actions on every push to the `main` branch.

### GitHub Configuration

1. Go to Settings > Pages
2. Source: GitHub Actions
3. The custom domain `blog.ignaciocano.com` is already configured in `static/CNAME`

## 📁 Project structure

```
.
├── .github/workflows/  # GitHub Actions
├── content/
│   ├── posts/         # Blog articles
│   └── search.md      # Search page
├── static/            # Static files (CNAME, etc.)
├── themes/PaperMod/   # Theme (submodule)
├── hugo.toml          # Hugo configuration
└── Makefile           # Useful commands
```

## 🔗 Legacy URLs

URLs follow the Pelican format for SEO compatibility:
```
/YYYY/MM/DD/slug/
```

Example: `/2026/02/19/migracion-pelican-a-hugo/`

## ⚙️ Available Make commands

```bash
make help           # Show help
make server         # Development server
make build          # Generate static site
make clean          # Clean generated files
make deploy         # Production build
make new-post       # Create a new post
make update-theme   # Update PaperMod theme
make install-hooks  # Install git hooks
```

## 🎣 Git Hooks

The project includes two git hooks. Install them with:

```bash
make install-hooks
```

### pre-commit
- Runs `hugo --quiet --minify` before each commit
- Validates there are no build errors
- Automatically cleans up generated files
- Prevents commits with syntax or configuration errors

### pre-push
- Checks if a newer Hugo version is available (via GitHub API)
- Shows a warning with the release URL if an update exists
- Never blocks the push (warning only)

### Skip hooks (emergencies only)
```bash
git commit --no-verify -m "message"
git push --no-verify
```

## 🔍 Features

- ✅ Integrated search with Fuse.js
- ✅ Pelican legacy URLs
- ✅ Responsive design
- ✅ Syntax highlighting
- ✅ RSS feed
- ✅ Tags and categories
- ✅ Automatic deploy with GitHub Actions
- ✅ Custom domain

## 📄 License

Content: All rights reserved © Nacho Cano
