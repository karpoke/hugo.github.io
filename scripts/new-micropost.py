#!/usr/bin/env python3
"""
Creates a micropost from a URL.
Automatically detects whether it is a YouTube video or a regular web article.

Usage:
    python3 scripts/new-micropost.py <URL>
    python3 scripts/new-micropost.py <URL> --draft
"""

import html as html_module
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

POSTS_DIR = Path(__file__).parent.parent / "content" / "posts" / "micropost"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"ERROR fetching {url}: {e}", file=sys.stderr)
        sys.exit(1)


def unescape(text: str) -> str:
    """Decode HTML entities and strip whitespace."""
    return html_module.unescape(text).strip()


def json_str(html: str, key: str) -> str | None:
    """Extract the value of a JSON key from HTML, decoding escape sequences."""
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"((?:[^"\\]|\\.)*)"', html)
    if not m:
        return None
    raw = m.group(1)
    # Decode \uXXXX and other JSON escapes
    try:
        value = json.loads(f'"{raw}"')
    except Exception:
        # Fallback: manually decode \uXXXX
        try:
            value = re.sub(
                r"\\u([0-9a-fA-F]{4})",
                lambda x: chr(int(x.group(1), 16)),
                raw,
            )
        except Exception:
            value = raw
    return unescape(value)


def meta(html: str, prop: str) -> str | None:
    """Extract the content of a meta tag (og:, name=, etc.)."""
    m = re.search(
        rf'<meta[^>]+(?:property|name)\s*=\s*["\']?{re.escape(prop)}["\']?[^>]+content\s*=\s*["\']([^"\']+)',
        html, re.IGNORECASE,
    ) or re.search(
        rf'<meta[^>]+content\s*=\s*["\']([^"\']+)[^>]+(?:property|name)\s*=\s*["\']?{re.escape(prop)}["\']?',
        html, re.IGNORECASE,
    )
    return unescape(m.group(1)) if m else None


def slugify(text: str) -> str:
    # Normalize Unicode characters to ASCII
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80]  # 80-character limit


def now_iso() -> str:
    tz = timezone(timedelta(hours=1))
    return datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S+01:00")


def extract_domain(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.removeprefix("www.")


def extract_yt_id(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if "youtube.com" in parsed.netloc:
        qs = urllib.parse.parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    if "youtu.be" in parsed.netloc:
        return parsed.path.lstrip("/")
    return None


def truncate_description(text: str, max_chars: int = 280) -> str:
    """Truncate to max_chars without splitting words, appending … if needed."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return truncated.rstrip(".,;:") + "…"


# ---------------------------------------------------------------------------
# Fetch metadata based on URL type
# ---------------------------------------------------------------------------

def get_youtube_metadata(url: str, video_id: str) -> dict:
    html = fetch(url)
    title = json_str(html, "title")
    author = json_str(html, "author")
    description = json_str(html, "shortDescription") or meta(html, "og:description")
    return {
        "title": unescape(title or "Untitled"),
        "author": unescape(author or "Unknown"),
        "description": truncate_description(unescape(description)) if description else None,
        "video_id": video_id,
        "domain": "youtube.com",
    }


def get_web_metadata(url: str) -> dict:
    html = fetch(url)

    # Title: og:title > <title> > json-ld
    title = (
        meta(html, "og:title")
        or json_str(html, "title")
        or re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL) and
           re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL).group(1).strip()
    )

    # Author: json-ld author > meta author > og:site_name
    author = (
        json_str(html, "author")
        or meta(html, "author")
        or meta(html, "article:author")
        or meta(html, "og:site_name")
        or extract_domain(url)
    )
    # If the author is in JSON object format {"name": "..."}, extract the name
    if author and author.startswith("{"):
        m = re.search(r'"name"\s*:\s*"([^"]+)"', author)
        if m:
            author = m.group(1)

    # Description: og:description > meta description > json-ld description
    description = (
        meta(html, "og:description")
        or meta(html, "description")
        or json_str(html, "description")
    )

    return {
        "title": unescape(title or "Untitled"),
        "author": unescape(author or extract_domain(url)).strip(),
        "description": truncate_description(unescape(description)) if description else None,
        "domain": extract_domain(url),
    }


# ---------------------------------------------------------------------------
# Generate the markdown file
# ---------------------------------------------------------------------------

def build_content(meta_data: dict, url: str, draft: bool) -> tuple[str, str]:
    title = meta_data["title"]
    author = meta_data["author"]
    description = meta_data.get("description")
    domain = meta_data["domain"]
    video_id = meta_data.get("video_id")
    slug = slugify(title)
    date = now_iso()
    safe_title = title.replace('"', '\\"')

    # Build blockquote
    if description:
        # Format to ~72 chars per line
        words = description.split()
        lines, current = [], ""
        for word in words:
            if current and len(current) + 1 + len(word) > 72:
                lines.append(f"> {current}")
                current = word
            else:
                current = f"{current} {word}".strip() if current else word
        if current:
            lines.append(f"> {current}")
        blockquote = "\n".join(lines)
    else:
        blockquote = f"> {title}"

    # Post body
    body_parts = [blockquote, ""]
    if video_id:
        body_parts += [f"{{{{< youtube {video_id} >}}}}", ""]

    body_parts += [
        f"» {author} | [{domain}][]",
        "",
        f"  [{domain}]: {url}",
        "",
    ]

    front_matter_lines = [
        "---",
        f'title: "{safe_title}"',
        f"date: {date}",
    ]
    if draft:
        front_matter_lines.append("draft: true")
    front_matter_lines += [
        'categories: ["micropost"]',
        "tags: []",
        f'slug: "{slug}"',
        "---",
    ]

    content = "\n".join(front_matter_lines) + "\n" + "\n".join(body_parts)
    return slug, content


def write_post(slug: str, content: str) -> Path:
    filepath = POSTS_DIR / f"{slug}.md"
    if filepath.exists():
        print(f"WARNING: file already exists: {filepath}", file=sys.stderr)
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Cancelled.", file=sys.stderr)
            sys.exit(0)
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]
    draft = "--draft" in flags or "-d" in flags

    if not args:
        print("Usage: new-micropost.py <URL> [--draft]", file=sys.stderr)
        sys.exit(1)

    url = args[0]
    print(f"Fetching metadata from: {url}")

    video_id = extract_yt_id(url)
    if video_id:
        print("Type: YouTube")
        meta_data = get_youtube_metadata(url, video_id)
    else:
        print("Type: web article")
        meta_data = get_web_metadata(url)

    print(f"  Title:   {meta_data['title']}")
    print(f"  Author:  {meta_data['author']}")
    if meta_data.get("description"):
        print(f"  Summary: {meta_data['description'][:60]}…")

    slug, content = build_content(meta_data, url, draft)
    filepath = write_post(slug, content)
    print(f"\nCreated: {filepath}")


if __name__ == "__main__":
    main()


