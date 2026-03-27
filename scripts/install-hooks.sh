#!/bin/bash
# Script to install project git hooks

echo "📦 Installing git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
if [ -f "scripts/pre-commit" ]; then
    cp scripts/pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✅ Pre-commit hook installed"
else
    echo "❌ Error: scripts/pre-commit not found"
    exit 1
fi

# Copy pre-push hook
if [ -f "scripts/pre-push" ]; then
    cp scripts/pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    echo "✅ Pre-push hook installed"
else
    echo "❌ Error: scripts/pre-push not found"
    exit 1
fi

echo ""
echo "🎉 Git hooks installed successfully"
echo ""
echo "The pre-commit hook will validate that Hugo can generate the site before each commit."
echo "The pre-push hook will check if a new Hugo version is available."
echo "To skip validation use: git commit --no-verify / git push --no-verify"
