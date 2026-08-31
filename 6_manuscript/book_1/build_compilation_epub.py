#!/usr/bin/env python3
"""Build the Book 1 SAMPLE epub: vetted first edition + the metric rewrites.

Two source formats, handled per chapter:
  - first_edition_clean/  : one line = one paragraph; '---' and bare '#' are
    scene breaks; a provenance HTML comment to strip.
  - rewrite_pilot/ drafts : blank-line paragraph separation; '---'/'#' breaks.
Each chapter page carries its provenance line under the heading.
"""
import re, html
from pathlib import Path
from ebooklib import epub

HERE = Path(__file__).resolve().parent
OUT = HERE / 'GoSquad_Book1_compilation.epub'
TITLE, AUTHOR, LANG = 'Go Squad', 'J. S. Vaughn', 'en'

CHAPTERS = [
    *[(f'Chapter {n}', HERE/'first_edition_clean'/f'chapter_{n:02d}.txt',
       'first edition · vetted') for n in range(1, 12)],
    ('Chapter 12', HERE/'rewrite_pilot'/'chapter_12_metric_v1.txt', 'metric rewrite'),
    ('Chapter 13', HERE/'rewrite_pilot'/'chapter_13_metric_v1.txt', 'metric rewrite'),
    ('Chapter 14', [HERE/'rewrite_pilot'/'chapter_14a_metric_v1.txt',
                    HERE/'rewrite_pilot'/'chapter_14b_metric_v1.txt'], 'metric rewrite'),
    ('Chapter 15', HERE/'rewrite_pilot'/'chapter_15_metric_v1.txt', 'metric rewrite'),
    ('Chapter 16', HERE/'rewrite_pilot'/'chapter_16_metric_v1.txt', 'metric rewrite'),
    ('Chapter 17', HERE/'rewrite_pilot'/'chapter_17_metric_v1.txt', 'metric rewrite'),
    ('Chapter 18', HERE/'rewrite_pilot'/'chapter_18_metric_v3.txt', 'metric rewrite'),
    ('Chapter 19', HERE/'rewrite_pilot'/'chapter_19_metric_v1.txt', 'metric rewrite'),
    ('Chapter 20', HERE/'rewrite_pilot'/'chapter_20_metric_v1.txt', 'metric rewrite'),
    ('Chapter 21', HERE/'rewrite_pilot'/'chapter_21_metric_v1.txt', 'metric rewrite'),
    ('Chapter 22', HERE/'rewrite_pilot'/'chapter_22_metric_v1.txt', 'metric rewrite'),
    ('Chapter 23', HERE/'rewrite_pilot'/'chapter_23_metric_v1.txt', 'metric rewrite'),
    ('Chapter 24', HERE/'rewrite_pilot'/'chapter_24_metric_v1.txt', 'metric rewrite'),
    ('Chapter 25', HERE/'rewrite_pilot'/'chapter_25_metric_v1.txt', 'metric rewrite'),
    ('Chapter 26', HERE/'rewrite_pilot'/'chapter_26_metric_v1.txt', 'metric rewrite'),
]

CSS = '''body { font-family: Georgia, serif; margin: 1em; line-height: 1.6; }
h1 { text-align: center; margin: 2em 0 0.2em; font-size: 1.5em; }
p.provenance { text-align: center; font-size: 0.8em; color: #888; font-style: italic; margin: 0 0 2em; text-indent: 0; }
p { text-indent: 1.5em; margin: 0.3em 0; }
p.scene-break { text-indent: 0; text-align: center; margin: 1.5em 0; }
.title-page { text-align: center; margin-top: 30%; }
.title-page h1 { font-size: 2em; }'''

BREAK = re.compile(r'^\s*(?:-{3,}|#)\s*$')
HEADER = re.compile(r'^\s*#\s*Chapter\s+\S+\s*$', re.I)


def blocks(path):
    t = re.sub(r'<!--.*?-->', '', path.read_text(encoding='utf-8'), flags=re.DOTALL)
    if '\n\n' in t.strip():   # draft format: blank-line paragraphs
        out = []
        for chunk in re.split(r'\n\s*\n', t):
            c = chunk.strip()
            if not c or HEADER.match(c):
                continue
            out.append(('break', None) if BREAK.match(c) else ('p', ' '.join(c.split())))
    else:                     # clean format: line = paragraph
        out = []
        for line in t.split('\n'):
            s = line.strip()
            if not s or HEADER.match(s):
                continue
            out.append(('break', None) if BREAK.match(s) else ('p', s))
    while out and out[0][0] == 'break': out.pop(0)
    while out and out[-1][0] == 'break': out.pop()
    return out


book = epub.EpubBook()
book.set_identifier('gosquad-book1-compilation')
book.set_title(TITLE); book.set_language(LANG); book.add_author(AUTHOR)
book.add_metadata('DC', 'description',
                  'Latest developed compilation: vetted first edition (1-11) + metric rewrites (12-21). Not for distribution.')
style = epub.EpubItem(uid='style', file_name='style/default.css',
                      media_type='text/css', content=CSS.encode())
book.add_item(style)
tp = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang=LANG)
tp.content = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head><body>
<div class="title-page"><h1>{TITLE}</h1><h2>by {AUTHOR}</h2>
<p style="margin-top:3em;font-style:italic;">Chapters 1–26</p>
<p style="font-style:italic;">Vetted first edition (1–11) + metric rewrites (12–26)</p>
<p style="font-style:italic;">Not for distribution</p></div></body></html>'''.encode()
tp.add_item(style); book.add_item(tp)

spine, toc, total = [tp], [], 0
for i, (name, path, prov) in enumerate(CHAPTERS, 1):
    paths = path if isinstance(path, list) else [path]
    bl = []
    for j, pp in enumerate(paths):
        if j: bl.append(('break', None))   # the 14a/14b seam becomes a scene break
        bl += blocks(pp)
    assert bl, f'EMPTY: {path}'
    words = sum(len(v.split()) for k, v in bl if k == 'p')
    total += words
    body = '\n'.join('<p class="scene-break">* * *</p>' if k == 'break'
                     else f'<p>{html.escape(v)}</p>' for k, v in bl)
    ch = epub.EpubHtml(title=name, file_name=f'ch{i:02d}.xhtml', lang=LANG)
    ch.content = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head><body>
<h1>{name}</h1><p class="provenance">{prov}</p>\n{body}</body></html>'''.encode()
    ch.add_item(style); book.add_item(ch); spine.append(ch); toc.append(ch)
    print(f'  {name:<12} {words:>5}w  ({prov})')

book.toc = toc
book.add_item(epub.EpubNcx()); book.add_item(epub.EpubNav())
book.spine = ['nav'] + spine
epub.write_epub(str(OUT), book, {})
print(f'\n{len(CHAPTERS)} chapters, ~{total} words\n{OUT}')
