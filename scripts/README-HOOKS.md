# Git Hooks - Documentation

## 🎯 Purpose

- **pre-commit**: Automatically validates that Hugo can generate the site before each commit, preventing syntax or configuration errors that would break the build.
- **pre-push**: Checks if a newer Hugo version is available before each push and warns if an update is pending.

## 📁 Files

### 1. `.git/hooks/pre-commit` (local, not tracked)
The active hook that git runs before each commit.

### 2. `.git/hooks/pre-push` (local, not tracked)
The active hook that git runs before each push.

### 3. `scripts/pre-commit` (tracked in repo)
Shareable source for the pre-commit hook.

### 4. `scripts/pre-push` (tracked in repo)
Shareable source for the pre-push hook.

### 5. `scripts/install-hooks.sh`
Installation script to set up both hooks easily.

## 🔧 Installation

For new developers cloning the repository:

```bash
make install-hooks
```

Or manually:
```bash
bash scripts/install-hooks.sh
```

## ✅ What does the pre-commit hook validate?

1. **Hugo is installed**: Verifies that the `hugo` command is available
2. **Successful build**: Runs `hugo --quiet --minify`
3. **No errors**: If there are syntax, configuration or content errors, the commit is rejected
4. **Auto cleanup**: Removes `public/` and `resources/` after validation

## 🚀 Workflow

```bash
# 1. Edit files
vim content/posts/my-post.md

# 2. Stage changes
git add content/posts/my-post.md

# 3. Attempt to commit
git commit -m "Add new post"

# 4. The hook runs automatically:
#    🔍 Pre-commit hook: Validating Hugo build...
#    ✅ Hugo build successful
#    [main abc1234] Add new post

# 5. If there are errors:
#    ❌ Error: Hugo build failed
#    [shows errors]
#    Commit rejected
```

## 🆘 Skip the hook (emergencies only)

In exceptional cases where you need to commit despite a failing build:

```bash
git commit --no-verify -m "WIP: work in progress"
```

**⚠️ Warning**: Only use in emergencies, as it may break the automatic deploy.

## 🧪 Test the hook manually

```bash
# Run the hook without committing
bash .git/hooks/pre-commit

# Or run the source script
bash scripts/pre-commit
```

## 📊 Output examples

### Successful build:
```
🔍 Pre-commit hook: Validating Hugo build...
✅ Hugo build successful
```

### Build with errors:
```
🔍 Pre-commit hook: Validating Hugo build...
❌ Error: Hugo build failed

Errors found:
ERROR the "date" front matter field is not a parsable date: see /path/to/post.md
ERROR render of "page" failed: template error

Please fix the errors before committing.
You can run 'hugo --verbose' for more details.
```

## 🔄 Update the hooks

If the hooks are updated in the repository:

```bash
make install-hooks  # Reinstall the latest version
```

## 🛠️ Customization

To modify a hook, edit the corresponding `scripts/` file and then run:

```bash
make install-hooks
```

## 📝 Benefits

- ✅ **Early detection**: Catches errors before committing
- ✅ **Faster CI/CD**: Avoids pushes that would fail in GitHub Actions
- ✅ **Consistency**: All developers use the same validation
- ✅ **Immediate feedback**: Errors reported in seconds, not minutes

## ❓ Troubleshooting

### Hook not running
```bash
# Check it exists and is executable
ls -la .git/hooks/pre-commit

# If missing, reinstall
make install-hooks
```

### Hugo not found
```bash
# Install Hugo
# See: https://gohugo.io/installation/
```

### Disable a hook permanently
```bash
# Rename the hook file
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
mv .git/hooks/pre-push .git/hooks/pre-push.disabled
```

---

## 🚀 pre-push hook: Hugo version check

### What does it do?

Before each `git push`, it queries the GitHub API to check if a newer Hugo version exists than the one installed locally. If so, it shows a warning with the release link and reminds you to update the workflow.

### Behaviour

- ✅ Hugo is up to date → push continues uninterrupted
- ⚠️ New version available → shows warning but **push continues** (not blocked)
- ⚠️ No internet or API failure → warning shown, push continues

### Output example

```
🔍 Pre-push hook: Checking Hugo version...
   Installed version: v0.159.0
   Latest version:    v0.160.0

⚠️  A new Hugo version is available: v0.160.0 (installed: v0.159.0)
   Update: https://github.com/gohugoio/hugo/releases/tag/v0.160.0
   Remember to also update HUGO_VERSION in .github/workflows/hugo.yml

   Push continues. Update Hugo when convenient.
```

### Skip the hook

```bash
\git push --no-verify
```

---

**Note**: Files in `.git/hooks/` are local and not tracked by git. That's why we include `scripts/pre-commit`, `scripts/pre-push` and `scripts/install-hooks.sh` in the repo so others can install them easily.
