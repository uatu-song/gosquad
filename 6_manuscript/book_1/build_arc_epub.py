#!/usr/bin/env python3
"""Build the Book 1 ARC — the shippable Advance Reader Copy.

Differs from build_compilation_epub.py, which is the WORKING artifact:
  - no provenance stamps anywhere (a reviewer never sees production metadata)
  - proper ARC front matter and an uncorrected-proof notice
  - series identification and reviewer-facing metadata
  - ch30's final section is promoted to a labelled Epilogue (the first edition
    marked it EPILOGUE; the rebuilt draft carries it as a scene break)
Text is byte-identical to the gated drafts. This script formats; it never edits.
"""
import re, html, datetime, subprocess
from pathlib import Path
from ebooklib import epub

HERE = Path(__file__).resolve().parent
OUT = HERE / 'GoSquad_Book1_ARC.epub'
TITLE  = 'Go Squad'
AUTHOR = 'J. S. Vaughn'
SERIES = 'The Auerbach Series'
BOOKNO = 1
LANG   = 'en'
STAMP  = datetime.date.today().isoformat()
try:
    REV = subprocess.run(['git','rev-parse','--short','HEAD'], cwd=HERE,
                         capture_output=True, text=True).stdout.strip() or 'local'
except Exception:
    REV = 'local'

CHAPTERS = [
    *[(f'Chapter {n}', HERE/'first_edition_clean'/f'chapter_{n:02d}.txt') for n in range(1, 12)],
    ('Chapter 12', HERE/'rewrite_pilot'/'chapter_12_metric_v1.txt'),
    ('Chapter 13', HERE/'rewrite_pilot'/'chapter_13_metric_v1.txt'),
    ('Chapter 14', [HERE/'rewrite_pilot'/'chapter_14a_metric_v1.txt',
                    HERE/'rewrite_pilot'/'chapter_14b_metric_v1.txt']),
    *[(f'Chapter {n}', HERE/'rewrite_pilot'/f'chapter_{n}_metric_v1.txt')
      for n in range(15, 31) if n != 18],
]
CHAPTERS.insert(17, ('Chapter 18', HERE/'rewrite_pilot'/'chapter_18_metric_v3.txt'))
CHAPTERS.sort(key=lambda c: int(re.search(r'\d+', c[0]).group()))

CSS = '''body { font-family: Georgia, "Times New Roman", serif; margin: 1.2em; line-height: 1.6; }
h1 { text-align: center; margin: 2.5em 0 1.6em; font-size: 1.4em; font-weight: normal;
     letter-spacing: 0.12em; text-transform: uppercase; }
p { text-indent: 1.4em; margin: 0; text-align: justify; }
p.first { text-indent: 0; }
p.scene-break { text-indent: 0; text-align: center; margin: 1.4em 0; letter-spacing: 0.4em; }
.tp { text-align: center; margin-top: 22%; }
.tp h1 { font-size: 2.1em; letter-spacing: 0.16em; margin-bottom: 0.6em; }
.tp .byline { font-size: 1.1em; font-style: italic; margin-bottom: 3.5em; }
.tp .series { font-size: 0.9em; letter-spacing: 0.18em; text-transform: uppercase; color: #555; }
.notice { margin: 12% 8%; font-size: 0.92em; line-height: 1.7; }
.notice h2 { text-align: center; font-size: 1em; letter-spacing: 0.18em;
             text-transform: uppercase; font-weight: normal; margin-bottom: 2em; }
.notice p { text-indent: 0; margin: 0 0 1.2em; text-align: left; }
.notice .stamp { font-size: 0.8em; color: #777; margin-top: 3em; }'''

BREAK  = re.compile(r'^\s*(?:-{3,}|#)\s*$')
HEADER = re.compile(r'^\s*#\s*Chapter\s+\S+\s*$', re.I)
EPI    = re.compile(r'^\s*EPILOGUE\s*$', re.I)


def blocks(path):
    t = re.sub(r'<!--.*?-->', '', path.read_text(encoding='utf-8'), flags=re.DOTALL)
    out = []
    chunks = re.split(r'\n\s*\n', t) if '\n\n' in t.strip() else t.split('\n')
    for chunk in chunks:
        c = chunk.strip()
        if not c or HEADER.match(c) or EPI.match(c):
            continue
        out.append(('break', None) if BREAK.match(c) else ('p', ' '.join(c.split())))
    while out and out[0][0] == 'break': out.pop(0)
    while out and out[-1][0] == 'break': out.pop()
    return out


def render(bl):
    parts, fresh = [], True
    for k, v in bl:
        if k == 'break':
            parts.append('<p class="scene-break">* * *</p>'); fresh = True
        else:
            cls = ' class="first"' if fresh else ''
            parts.append(f'<p{cls}>{html.escape(v)}</p>')
            fresh = False
    return '\n'.join(parts)


book = epub.EpubBook()
book.set_identifier(f'gosquad-book1-arc-{STAMP}')
book.set_title(TITLE); book.set_language(LANG); book.add_author(AUTHOR)
book.add_metadata('DC', 'description',
    f'ADVANCE READER COPY — uncorrected proof. {SERIES}, Book {BOOKNO}. '
    'Not for sale. Quotations must be checked against the finished book.')
book.add_metadata('DC', 'date', STAMP)
book.add_metadata(None, 'meta', '', {'name': 'calibre:series', 'content': SERIES})
book.add_metadata(None, 'meta', '', {'name': 'calibre:series_index', 'content': str(BOOKNO)})

style = epub.EpubItem(uid='style', file_name='style/default.css',
                      media_type='text/css', content=CSS.encode())
book.add_item(style)

def page(uid, fname, title, inner):
    it = epub.EpubHtml(title=title, file_name=fname, lang=LANG)
    it.content = ('<html><head><link rel="stylesheet" href="style/default.css"/></head>'
                  f'<body>{inner}</body></html>').encode()
    it.add_item(style); book.add_item(it); return it

tp = page('tp', 'title.xhtml', 'Title Page',
    f'<div class="tp"><h1>{TITLE}</h1><p class="byline">{AUTHOR}</p>'
    f'<p class="series">{SERIES} &#183; Book One</p></div>')

notice = page('notice', 'notice.xhtml', 'Advance Reader Copy',
    '<div class="notice"><h2>Advance Reader Copy</h2>'
    '<p>This is an uncorrected proof. It is not the finished book.</p>'
    '<p>Text, chapter order and front matter may change before publication. '
    'Any quotation intended for review or publicity must be checked against the '
    'final published edition.</p>'
    '<p>Not for sale, resale, or redistribution.</p>'
    f'<p class="stamp">{SERIES} &#183; Book {BOOKNO}<br/>'
    f'Proof generated {STAMP} &#183; build {REV}</p></div>')

spine, toc, total = [tp, notice], [], 0
for i, (name, path) in enumerate(CHAPTERS, 1):
    paths = path if isinstance(path, list) else [path]
    bl = []
    for j, pp in enumerate(paths):
        if j: bl.append(('break', None))
        bl += blocks(pp)
    assert bl, f'EMPTY: {path}'

    # ch30: promote the final section to a labelled Epilogue
    epi = None
    if name == 'Chapter 30':
        idx = max(k for k, (t, _) in enumerate(bl) if t == 'break')
        bl, epi = bl[:idx], bl[idx+1:]

    words = sum(len(v.split()) for k, v in bl if k == 'p')
    ch = page(f'c{i}', f'ch{i:02d}.xhtml', name, f'<h1>{name}</h1>\n{render(bl)}')
    spine.append(ch); toc.append(ch); total += words
    line = f'  {name:<12} {words:>5}w'

    if epi:
        ew = sum(len(v.split()) for k, v in epi if k == 'p')
        ep = page('epi', 'epilogue.xhtml', 'Epilogue', f'<h1>Epilogue</h1>\n{render(epi)}')
        spine.append(ep); toc.append(ep); total += ew
        line += f'\n  {"Epilogue":<12} {ew:>5}w'
    print(line)

book.toc = toc
book.add_item(epub.EpubNcx()); book.add_item(epub.EpubNav())
book.spine = ['nav'] + spine
epub.write_epub(str(OUT), book, {})
print(f'\nARC: {len(CHAPTERS)} chapters + epilogue, ~{total:,} words')
print(f'{OUT}  ({OUT.stat().st_size//1024} KB)  build {REV}  {STAMP}')
