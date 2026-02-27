#!/usr/bin/env python3
"""
Create a new blog post organized by publication date.
Posts are saved in: content/posts/YYYY/MM/post-slug.md

Usage:
    python3 scripts/new-post.py "Post Title" "category"
    python3 scripts/new-post.py "My Post" "dev"

Valid categories: admin, dev, hack, memo
"""

import sys
import re
import unicodedata
from datetime import datetime, timezone, timedelta
from pathlib import Path

POSTS_DIR = Path('content/posts')
VALID_CATEGORIES = ['admin', 'dev', 'hack', 'memo']


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    # Normalize Unicode characters to ASCII
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80]


def now_iso() -> str:
    """Get current date/time in ISO format."""
    tz = timezone(timedelta(hours=1))
    return datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S+01:00")


def create_post(title: str, category: str) -> None:
    """Create a new blog post."""
    if not title:
        print("Error: Title is required", file=sys.stderr)
        sys.exit(1)

    if not category or category not in VALID_CATEGORIES:
        print(f"Error: Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}", file=sys.stderr)
        sys.exit(1)

    # Get current date
    now = datetime.now(timezone(timedelta(hours=1)))
    year = now.strftime("%Y")
    month = now.strftime("%m")

    # Create directory structure
    post_dir = POSTS_DIR / year / month
    post_dir.mkdir(parents=True, exist_ok=True)

    # Create filename and path
    slug = slugify(title)
    filepath = post_dir / f"{slug}.md"

    # Check if file exists
    if filepath.exists():
        print(f"Error: File already exists: {filepath}", file=sys.stderr)
        sys.exit(1)

    # Create frontmatter
    date_str = now_iso()
    safe_title = title.replace('"', '\\"')

    content = f'''---
title: "{safe_title}"
date: {date_str}
categories: ["{category}"]
tags: []
slug: "{slug}"
description: ""
---

## 

'''

    # Write file
    filepath.write_text(content, encoding='utf-8')
    print(f"✓ Created: {filepath}")
    print(f"  Edit the file to add content and description")


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: new-post.py <TITLE> <CATEGORY>", file=sys.stderr)
        print(f"Valid categories: {', '.join(VALID_CATEGORIES)}", file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1]
    category = sys.argv[2]

    create_post(title, category)


if __name__ == "__main__":
    main()



