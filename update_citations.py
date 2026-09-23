#!/usr/bin/env python3
"""
update_citations.py
───────────────────
Fetches live citation stats from Google Scholar and updates index.html.

Usage:
    pip install scholarly        # one-time install
    python update_citations.py   # run whenever you want to refresh

The script is safe to re-run: if Scholar is unreachable it exits
without modifying the file, so your existing numbers stay intact.
"""

import re
import sys
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────────────────

SCHOLAR_ID = "0jB6u6kAAAAJ"
HTML_FILE  = Path(__file__).parent / "index.html"

# ── Fetch ─────────────────────────────────────────────────────────────────────

def fetch_stats(scholar_id: str) -> dict:
    try:
        from scholarly import scholarly as sc
    except ImportError:
        sys.exit("scholarly not installed — run:  pip install scholarly")

    print(f"Fetching Google Scholar profile [{scholar_id}] …")
    try:
        author = sc.search_author_id(scholar_id)
        author = sc.fill(author, sections=["basics", "indices"])
    except Exception as e:
        sys.exit(f"Could not reach Google Scholar: {e}")

    citations = author.get("citedby")
    hindex    = author.get("hindex")
    i10index  = author.get("i10index")

    if citations is None:
        sys.exit("Fetched profile but citation count was empty — aborting.")

    return {"citations": citations, "hindex": hindex, "i10index": i10index}

# ── Patch HTML ────────────────────────────────────────────────────────────────

def update_html(stats: dict, html_path: Path) -> None:
    citations_fmt = f"{stats['citations']:,}"
    hindex_str    = str(stats["hindex"])

    html = html_path.read_text(encoding="utf-8")

    en_pattern = r'[\d,]+ citations (&middot; <em>h</em>-index: )\d+'
    zh_pattern = r'[\d,]+ 次引用 (&middot; <em>h</em> 指数：)\d+'

    if not re.search(en_pattern, html) and not re.search(zh_pattern, html):
        print("⚠  No patterns matched — check that index.html is in the same folder.")
        return

    html = re.sub(en_pattern, rf'{citations_fmt} citations \g<1>{hindex_str}', html)
    html = re.sub(zh_pattern, rf'{citations_fmt} 次引用 \g<1>{hindex_str}', html)

    html_path.write_text(html, encoding="utf-8")
    print(f"✓  index.html updated  ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"   Citations : {citations_fmt}")
    print(f"   h-index   : {hindex_str}")
    if stats["i10index"] is not None:
        print(f"   i10-index : {stats['i10index']}")

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    stats = fetch_stats(SCHOLAR_ID)
    update_html(stats, HTML_FILE)
