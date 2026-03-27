#!/usr/bin/env python3
"""
Import bookmarks from a saved-YYYY.json file into Hugo microposts.
Fetches each URL to extract summary, author, and tags.

Usage:
    python3 scripts/import-bookmarks.py static/bookmarks/saved-2026.json [--dry-run]
"""

import html as html_module
import json
import re
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

POSTS_DIR = Path('content/posts')
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Meneame external URL pattern
MENEAME_URL_PATTERN = re.compile(r'<h2>\s*<a\s+href="([^"]+)"\s+class="l:\d+')


# ---------------------------------------------------------------------------
# Helpers (adapted from new-micropost.py)
# ---------------------------------------------------------------------------

def fetch(url: str) -> str:
    """Fetch URL content with SSL context and retries."""
    ctx = ssl.create_default_context()
    encoded = encode_url(url)
    req = urllib.request.Request(encoded, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                raise RuntimeError(f"Failed to fetch {url}: {e}")


def encode_url(url: str) -> str:
    """Properly encode non-ASCII characters in URL path."""
    parsed = urllib.parse.urlparse(url.strip())
    encoded_path = urllib.parse.quote(parsed.path, safe='/:@!$&\'()*+,;=-._~')
    return urllib.parse.urlunparse(parsed._replace(path=encoded_path))


def unescape(text: str) -> str:
    return html_module.unescape(text).strip()


def json_str(html: str, key: str) -> str | None:
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"((?:[^"\\]|\\.)*)"', html)
    if not m:
        return None
    raw = m.group(1)
    try:
        value = json.loads(f'"{raw}"')
    except Exception:
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
    m = re.search(
        rf'<meta[^>]+(?:property|name)\s*=\s*["\']?{re.escape(prop)}["\']?[^>]+content\s*=\s*["\']([^"\']+)',
        html, re.IGNORECASE,
    ) or re.search(
        rf'<meta[^>]+content\s*=\s*["\']([^"\']+)[^>]+(?:property|name)\s*=\s*["\']?{re.escape(prop)}["\']?',
        html, re.IGNORECASE,
    )
    return unescape(m.group(1)) if m else None


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80].strip("-")


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
    text = text.strip()
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return truncated.rstrip(".,;:") + "…"


def is_meneame(url: str) -> bool:
    return "meneame.net" in urllib.parse.urlparse(url).netloc


def resolve_meneame(url: str, html: str) -> str | None:
    """Extract the external URL from a meneame page."""
    m = MENEAME_URL_PATTERN.search(html)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Tag extraction with broader keyword set
# ---------------------------------------------------------------------------

KEYWORDS = {
    'python': r'\bpython\b',
    'javascript': r'\bjavascript\b|\bjs\b',
    'typescript': r'\btypescript\b',
    'django': r'\bdjango\b',
    'react': r'\breact\b',
    'vue': r'\bvue\b',
    'docker': r'\bdocker\b',
    'kubernetes': r'\bkubernetes\b|\bk8s\b',
    'git': r'\bgit\b',
    'sql': r'\bsql\b',
    'postgresql': r'\bpostgres(?:ql)?\b',
    'mysql': r'\bmysql\b',
    'database': r'\bdatabas(?:e|es)\b|\bbase[s]?\s*de\s*datos\b',
    'linux': r'\blinux\b|\bubuntu\b|\bdebian\b',
    'security': r'\bsecurity\b|\bcybersecurity\b|\bciberseguridad\b|\bseguridad\b',
    'privacy': r'\bprivacy\b|\bprivacidad\b',
    'api': r'\bapi\b|\brest\b',
    'web': r'\bweb\b|\bhtml\b|\bcss\b',
    'backend': r'\bbackend\b',
    'frontend': r'\bfrontend\b',
    'devops': r'\bdevops\b',
    'testing': r'\btesting\b|\btdd\b|\bunit\s*test\b',
    'performance': r'\bperformance\b|\brendimiento\b',
    'optimization': r'\boptimiz\w+\b|\boptimiz\w+\b',
    'tutorial': r'\btutorial\b|\bguide\b|\bguía\b',
    'ai': r'\bartificial\s*intelligen\w+\b|\binteligencia\s*artificial\b|\b(?:^|\s)ia(?:\s|$)\b|\bmachine\s*learning\b',
    'open-source': r'\bopen\s*source\b|\bcódigo\s*abierto\b|\bfree\s*software\b|\bsoftware\s*libre\b',
    'microservices': r'\bmicroservic\w+\b',
    'debugging': r'\bdebugg?\w+\b|\bdepura\w+\b',
    'networking': r'\bnetwork\w+\b|\bdns\b|\btcp\b|\bip\b',
    'science': r'\bscien\w+\b|\bciencia\b|\bfísica\b|\bphysics\b|\bthermodyn\w+\b|\btermodinám\w+\b',
    'biology': r'\bbiol\w+\b|\bvirus\b|\bprion\w+\b|\bviroide\w+\b',
    'retro': r'\bretro\b|\bemulador\w*\b|\bemulator\w*\b',
    'gaming': r'\bgaming\b|\bjuego\w*\b|\bgame\w*\b',
    'whatsapp': r'\bwhatsapp\b',
    'programming': r'\bprogramm\w+\b|\bprogramaci\w+\b|\bcoding\b',
    'dynamic-programming': r'\bdynamic\s*programming\b|\bprogramación\s*dinámica\b',
    'webgl': r'\bwebgl\b|\bshader\w*\b|\bopengl\b',
    'history': r'\bhistor\w+\b|\b1995\b',
    'podcast': r'\bpodcast\b',
    'vscode': r'\bvs\s*code\b|\bvscode\b',
}


def extract_tags(title: str, description: str = "", html: str = "") -> list[str]:
    """Extract up to 3 relevant tags from title, description and content."""
    combined = (title + " " + description).lower()

    found = []
    for tag, pattern in KEYWORDS.items():
        if re.search(pattern, combined, re.IGNORECASE):
            found.append(tag)
        if len(found) >= 3:
            break

    return found[:3]


# ---------------------------------------------------------------------------
# Metadata extraction
# ---------------------------------------------------------------------------

def get_youtube_metadata(url: str, video_id: str, html: str) -> dict:
    title = json_str(html, "title")
    author = json_str(html, "author")
    description = json_str(html, "shortDescription") or meta(html, "og:description")
    tags = extract_tags(title or "Untitled", description or "", html)
    return {
        "title": unescape(title or "Untitled"),
        "author": unescape(author or "Unknown"),
        "description": truncate_description(unescape(description)) if description else None,
        "video_id": video_id,
        "domain": "youtube.com",
        "tags": tags,
    }


def get_web_metadata(url: str, html: str) -> dict:
    # Title
    title = meta(html, "og:title") or json_str(html, "title")
    if not title:
        m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if m:
            title = m.group(1).strip()

    # Author
    author = None
    author = json_str(html, "author")
    if author and author.startswith("{"):
        m = re.search(r'"name"\s*:\s*"([^"]+)"', author)
        author = m.group(1) if m else None

    if not author:
        author = (
            meta(html, "author")
            or meta(html, "article:author")
            or meta(html, "article.author")
        )

    if not author:
        m = re.search(r'<[^>]*class=["\'].*?byline.*?["\'][^>]*>([^<]+)</[^>]*>', html, re.IGNORECASE)
        if m:
            author = m.group(1).strip()

    if not author:
        m = re.search(r'<(?:span|div)[^>]*class=["\'](?:author|writer)["\'][^>]*>([^<]+)</(?:span|div)>', html, re.IGNORECASE)
        if m:
            author = m.group(1).strip()

    if not author:
        m = re.search(r'<[^>]*itemprop\s*=\s*["\']author["\'][^>]*>([^<]+)</[^>]*>', html, re.IGNORECASE)
        if m:
            author = m.group(1).strip()

    if not author:
        author = meta(html, "og:site_name") or extract_domain(url)

    # Description
    description = (
        meta(html, "og:description")
        or meta(html, "description")
        or json_str(html, "description")
    )

    tags = extract_tags(title or "Untitled", description or "", html)

    return {
        "title": unescape(title or "Untitled"),
        "author": unescape(author or extract_domain(url)).strip(),
        "description": truncate_description(unescape(description)) if description else None,
        "domain": extract_domain(url),
        "tags": tags,
    }


# ---------------------------------------------------------------------------
# Post generation
# ---------------------------------------------------------------------------

def build_content(meta_data: dict, url: str, date: str) -> tuple[str, str]:
    title = meta_data["title"]
    author = meta_data["author"]
    description = meta_data.get("description")
    domain = meta_data["domain"]
    video_id = meta_data.get("video_id")
    tags = meta_data.get("tags", [])
    slug = slugify(title)
    safe_title = title.replace('"', '\\"')

    # Build blockquote
    if description:
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

    body_parts = [blockquote, ""]
    if video_id:
        body_parts += [f"{{{{< youtube {video_id} >}}}}", ""]

    body_parts += [
        f"» {author} | [{domain}][]",
        "",
        f"  [{domain}]: {url}",
        "",
    ]

    tags_str = json.dumps(tags) if tags else "[]"

    front_matter_lines = [
        "---",
        f'title: "{safe_title}"',
        f"date: {date}",
        'categories: ["micropost"]',
        f"tags: {tags_str}",
        f'slug: "{slug}"',
        "---",
    ]

    content = "\n".join(front_matter_lines) + "\n" + "\n".join(body_parts)
    return slug, content


def write_post(slug: str, content: str, date: str, dry_run: bool = False) -> Path | None:
    dt = datetime.fromisoformat(date)
    year = dt.strftime("%Y")
    month = dt.strftime("%m")

    post_dir = POSTS_DIR / year / month
    filepath = post_dir / f"{slug}.md"

    if filepath.exists():
        print(f"  SKIP (already exists): {filepath}")
        return None

    if dry_run:
        print(f"  DRY-RUN would create: {filepath}")
        return filepath

    post_dir.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]
    dry_run = "--dry-run" in flags

    if not args:
        print("Usage: import-bookmarks.py <json-file> [--dry-run]", file=sys.stderr)
        sys.exit(1)

    json_path = Path(args[0])
    if not json_path.exists():
        print(f"ERROR: File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(json_path.read_text(encoding='utf-8'))
    bookmarks = data.get("bookmarks", [])
    print(f"Found {len(bookmarks)} bookmarks in {json_path}")

    created = 0
    skipped = 0
    errors = 0

    for i, bm in enumerate(bookmarks, 1):
        title = bm["title"]
        canonical_title = unescape(title).strip()
        url = bm["url"].strip()
        date = bm["date"]

        print(f"\n[{i}/{len(bookmarks)}] {title}")
        print(f"  URL: {url}")

        try:
            # Handle meneame URLs: resolve to actual article
            actual_url = url
            if is_meneame(url):
                print("  Resolving meneame URL...")
                meneame_html = fetch(url)
                resolved = resolve_meneame(url, meneame_html)
                if resolved:
                    actual_url = resolved
                    print(f"  Resolved to: {actual_url}")
                else:
                    print("  WARNING: Could not resolve meneame URL, using original")

            # Fetch actual page
            html = fetch(actual_url)

            # Detect type and extract metadata
            video_id = extract_yt_id(actual_url)
            if video_id:
                meta_data = get_youtube_metadata(actual_url, video_id, html)
            else:
                meta_data = get_web_metadata(actual_url, html)

            # Override title from bookmark if the fetched one is generic
            if meta_data["title"] in ("Untitled", "") or len(meta_data["title"]) < 5:
                meta_data["title"] = title

            # Keep bookmark title as canonical to avoid generic page titles like "Artículos".
            if canonical_title:
                meta_data["title"] = canonical_title

            print(f"  Author: {meta_data['author']}")
            print(f"  Tags: {meta_data.get('tags', [])}")
            if meta_data.get("description"):
                print(f"  Summary: {meta_data['description'][:80]}...")

            slug, content = build_content(meta_data, actual_url, date)
            filepath = write_post(slug, content, date, dry_run)

            if filepath:
                print(f"  Created: {filepath}")
                created += 1
            else:
                skipped += 1

        except Exception as e:
            print(f"  WARNING: Could not fetch URL: {e}", file=sys.stderr)
            print(f"  Using bookmark title as fallback...")
            # Create post with fallback metadata from the bookmark itself
            fallback_meta = {
                "title": canonical_title or title,
                "author": extract_domain(url),
                "description": None,
                "domain": extract_domain(url),
                "tags": extract_tags(canonical_title or title, ""),
            }
            slug, content = build_content(fallback_meta, url, date)
            filepath = write_post(slug, content, date, dry_run)
            if filepath:
                print(f"  Created (fallback): {filepath}")
                created += 1
            else:
                skipped += 1

        # Be polite to servers
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"Done! Created: {created}, Skipped: {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()

