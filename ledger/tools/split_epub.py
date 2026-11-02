#!/usr/bin/env python3
"""
split_epub.py — turn a compiled EPUB into one plain-text file per chapter.

Use ONLY if the book exists in this repo as a compiled EPUB and nothing finer.
If the repo already has chapter files, point suite.prose_globs at those instead.

Output convention (what every suite tool expects):
  - one file per chapter document, named from its heading: CH01.txt, CH02.txt …
    (or --names keeps a slug: CH01_Title.txt)
  - one paragraph per line; NO blank lines between paragraphs
  - a single blank line marks a scene break (<hr>, "* * *", "#", "***")
  - <em>/<i> become *asterisks*; headings are dropped (the filename carries the id)
  - typography is left EXACTLY as the EPUB has it (mixed straight/curly stays mixed —
    census it with check_typography.py --census before any conversion)

Usage:
  python3 ledger/tools/split_epub.py BOOK.epub chapters/            # dry run: lists what it would write
  python3 ledger/tools/split_epub.py BOOK.epub chapters/ --write    # writes; refuses to overwrite
Chapter ids come from the headings ("Chapter 7" -> CH07, Prologue -> PR, Epilogue -> EP);
other documents are skipped and listed. --all numbers every headed document instead.
"""
import html, os, re, sys, zipfile

def spine_docs(z):
    opf = next(n for n in z.namelist() if n.endswith(".opf"))
    o = z.read(opf).decode("utf-8", "ignore")
    base = opf.rsplit("/", 1)[0] + "/" if "/" in opf else ""
    items = {}
    for m in re.finditer(r"<item\b[^>]*>", o):
        tag = m.group(0)
        i = re.search(r'\bid="([^"]+)"', tag); h = re.search(r'\bhref="([^"]+)"', tag)
        if i and h: items[i.group(1)] = base + h.group(1)
    return [items[i] for i in re.findall(r'<itemref\b[^>]*idref="([^"]+)"', o) if i in items]

def paras(xhtml):
    body = re.sub(r"(?is)^.*?<body[^>]*>|</body>.*$", "", xhtml)
    body = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", body)
    heading = re.search(r"(?is)<h[1-3][^>]*>(.*?)</h[1-3]>", body)
    title = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip() if heading else ""
    body = re.sub(r"(?is)<h[1-6][^>]*>.*?</h[1-6]>", "", body)
    body = re.sub(r"(?is)<hr\b[^>]*>", "\n<p>#SCENE#</p>\n", body)
    out = []
    for m in re.finditer(r"(?is)<p\b[^>]*>(.*?)</p>", body):
        t = m.group(1)
        t = re.sub(r"(?is)</?(?:em|i)\b[^>]*>", "*", t)
        t = re.sub(r"(?is)<br\s*/?>", " ", t)
        t = html.unescape(re.sub(r"<[^>]+>", "", t))
        t = re.sub(r"\s+", " ", t).strip().replace("**", "")
        if not t: continue
        if t in ("#SCENE#", "#", "* * *", "***", "*", "⁂"):
            if out and out[-1] != "": out.append("")
            continue
        out.append(t)
    while out and out[-1] == "": out.pop()
    return title, out

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    src, dest = sys.argv[1], sys.argv[2]
    write, names = "--write" in sys.argv, "--names" in sys.argv
    z = zipfile.ZipFile(src)
    keep_all = "--all" in sys.argv
    n = 0; plan = []
    for doc in spine_docs(z):
        title, ps = paras(z.read(doc).decode("utf-8", "ignore"))
        m = re.match(r"(?i)^\s*chapter\s+(\d+)\b", title or "")
        if m:
            cid = f"CH{int(m.group(1)):02d}"
        elif re.match(r"(?i)^\s*prologue\b", title or ""):
            cid = "PR"
        elif re.match(r"(?i)^\s*epilogue\b", title or ""):
            cid = "EP"
        elif keep_all and title and ps:
            n += 1; cid = f"CH{n:02d}"
        else:
            print(f"  skip  {doc}  ({title or 'no heading'}; {len(ps)} paras) — not a 'Chapter N' heading (--all to number every document)")
            continue
        if not ps:
            print(f"  skip  {doc}  ({title}; no paragraphs)"); continue
        slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")[:40]
        fn = cid + (f"_{slug}" if names else "") + ".txt"
        if any(fn == x[0] for x in plan):
            sys.exit(f"REFUSED: two documents map to {fn} — check the headings")
        plan.append((fn, title, ps))
        print(f"  {cid:5} {len(ps):4} paras  {sum(len(p.split()) for p in ps):6} words  ← {doc}  [{title}]")
    if not write:
        print(f"\nDRY RUN — {len(plan)} chapters. Check the list (front/back matter skipped?), then rerun with --write.")
        return 0
    os.makedirs(dest, exist_ok=True)
    clash = [fn for fn, _, _ in plan if os.path.exists(os.path.join(dest, fn))]
    if clash:
        sys.exit(f"REFUSED: would overwrite {clash[:5]}… in {dest}. Move them first.")
    for fn, title, ps in plan:
        open(os.path.join(dest, fn), "w", encoding="utf-8").write("\n".join(ps) + "\n")
    print(f"\nWROTE {len(plan)} chapter files to {dest}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
