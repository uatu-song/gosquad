#!/usr/bin/env python3
"""Render GoSquad_Book1_v<VERSION>.epub to a single Markdown file.

Output: GoSquad_Book1_v<VERSION>.md next to the epub. Same text, same version
stamp. Run after build_review_epub.py. Any older GoSquad_Book1_v*.md is moved
to _archive/epubs/. This script formats; it never edits.
"""
import html, re, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERSION = (HERE / "REVIEW_VERSION").read_text().strip()
EPUB = HERE / f"GoSquad_Book1_v{VERSION}.epub"
OUT = HERE / f"GoSquad_Book1_v{VERSION}.md"

def text(fragment):
    fragment = re.sub(r"</?(?:i|em)>", "*", fragment)
    return html.unescape(re.sub(r"<br\s*/?>", "  \n", re.sub(r"</?(?!br)[^>]+>", "", fragment))).strip()

z = zipfile.ZipFile(EPUB)
files = ["EPUB/notice.xhtml"] + sorted(n for n in z.namelist() if re.fullmatch(r"EPUB/ch\d+\.xhtml", n)) + ["EPUB/epilogue.xhtml"]

out = ["# Go Squad", "", "*J. S. Vaughn* · Book One", ""]
for name in files:
    body = z.read(name).decode().split("<body>", 1)[1]
    for tag, cls, inner in re.findall(r'<(h1|h2|p)(?: class="([^"]*)")?>(.*?)</\1>', body, re.S):
        t = text(inner)
        if tag in ("h1", "h2"):
            out += ["---" if name == files[1] or tag == "h2" else "", "", f"## {t}", ""]
        elif cls == "scene-break":
            out += ["* * *", ""]
        elif cls == "stamp":
            out += [f"*{t}*", ""]
        else:
            out += [t, ""]

for old in HERE.glob("GoSquad_Book1_v*.md"):
    if old != OUT:
        (HERE / "_archive" / "epubs").mkdir(parents=True, exist_ok=True)
        old.rename(HERE / "_archive" / "epubs" / old.name)
        print(f"archived {old.name} -> _archive/epubs/")
OUT.write_text(re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {len(OUT.read_text().split()):,} words)")
