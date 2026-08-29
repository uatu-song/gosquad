#!/usr/bin/env python3
"""Build Book 1 EPUB from the CLEAN first-edition chapter files.

Source: 6_manuscript/book_1/first_edition_clean/ (registered as `book_1_clean`,
the measurement ground truth) — NOT book1_manuscript.txt, which is the damaged
PDF extraction this script used to read (318 running headers, 418 broken words,
paragraph structure collapsed).

The old GoSquad_Book1.epub is left in place: it is the stated ancestor of
6_manuscript/book_1/first_edition/ (registered as `book_1_ed1`), and quarry
lineage is translated on ingest, never overwritten.
"""

import re
import html
from pathlib import Path

from ebooklib import epub

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / 'first_edition_clean'
OUTPUT = HERE / 'GoSquad_Book1_clean.epub'

CHAPTER_GLOB = 'chapter_*.txt'
CHAPTER_NUM_RE = re.compile(r'chapter_(\d+)')

# Scene-break markers used in the clean source. Both forms appear; they mean
# the same thing (30 '---' lines and a number of bare '#' lines).
SCENE_BREAK_RE = re.compile(r'^\s*(?:-{3,}|#)\s*$')
# The per-file title header, e.g. "# Chapter 7". Must be tested BEFORE the
# scene-break rule, which would otherwise swallow it.
TITLE_RE = re.compile(r'^\s*#\s*Chapter\s+(\d+)\s*$', re.IGNORECASE)
# The provenance comment each clean chapter carries.
COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)

TITLE = 'Go Squad'
AUTHOR = 'J. S. Vaughn'
LANG = 'en'

CSS = '''
body { font-family: Georgia, serif; margin: 1em; line-height: 1.6; }
h1 { text-align: center; margin-top: 2em; margin-bottom: 1em; font-size: 1.5em; }
p { text-indent: 1.5em; margin: 0.3em 0; }
p.scene-break { text-indent: 0; text-align: center; margin: 1.5em 0; }
.title-page { text-align: center; margin-top: 30%; }
.title-page h1 { font-size: 2em; }
.title-page h2 { font-size: 1.2em; font-weight: normal; margin-top: 1em; }
'''


def load_chapters(input_dir):
    """Read the clean per-chapter files, ordered by chapter number.

    Each chapter is returned as (num, blocks), where blocks is a list of
    ('p', text) and ('break', None) tuples. In the clean source ONE LINE IS ONE
    PARAGRAPH -- there are no blank-line paragraph separators (2 blank lines per
    file, both around the provenance comment), so splitting on double newlines
    the way the old script did would collapse each chapter into a single <p>.
    """
    paths = sorted(
        input_dir.glob(CHAPTER_GLOB),
        key=lambda p: int(CHAPTER_NUM_RE.search(p.name).group(1)),
    )

    chapters = []
    for path in paths:
        num = int(CHAPTER_NUM_RE.search(path.name).group(1))
        text = COMMENT_RE.sub('', path.read_text(encoding='utf-8'))

        blocks = []
        for line in text.splitlines():
            if not line.strip():
                continue
            if TITLE_RE.match(line):          # the "# Chapter N" header
                continue
            if SCENE_BREAK_RE.match(line):
                blocks.append(('break', None))
            else:
                blocks.append(('p', line.strip()))

        # A scene break at either edge is an artifact, not a beat.
        while blocks and blocks[0][0] == 'break':
            blocks.pop(0)
        while blocks and blocks[-1][0] == 'break':
            blocks.pop()

        chapters.append((num, blocks))

    return chapters


def blocks_to_html(blocks):
    parts = []
    for kind, value in blocks:
        if kind == 'break':
            parts.append('<p class="scene-break">* * *</p>')
        else:
            parts.append(f'<p>{html.escape(value)}</p>')
    return '\n'.join(parts)


def build_epub(chapters):
    book = epub.EpubBook()

    book.set_identifier('gosquad-book1-clean')
    book.set_title(TITLE)
    book.set_language(LANG)
    book.add_author(AUTHOR)
    book.add_metadata('DC', 'description',
                      'Advanced Reader Copy — Not for distribution. '
                      'Built from the clean first-edition source.')

    style = epub.EpubItem(
        uid='style',
        file_name='style/default.css',
        media_type='text/css',
        content=CSS.encode('utf-8'),
    )
    book.add_item(style)

    title_html = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head>
<body>
<div class="title-page">
<h1>{TITLE}</h1>
<h2>by {AUTHOR}</h2>
<p style="margin-top: 3em; font-style: italic;">Advanced Reader Copy</p>
<p style="font-style: italic;">Not for distribution</p>
</div>
</body></html>'''
    title_page = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang=LANG)
    title_page.content = title_html.encode('utf-8')
    title_page.add_item(style)
    book.add_item(title_page)

    epub_chapters = [title_page]
    toc = []

    for num, blocks in chapters:
        ch_title = f'Chapter {num}'
        ch = epub.EpubHtml(
            title=ch_title,
            file_name=f'chapter_{num:02d}.xhtml',
            lang=LANG,
        )
        ch.content = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head>
<body>
<h1>{ch_title}</h1>
{blocks_to_html(blocks)}
</body></html>'''.encode('utf-8')
        ch.add_item(style)
        book.add_item(ch)
        epub_chapters.append(ch)
        toc.append(ch)

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + epub_chapters

    epub.write_epub(str(OUTPUT), book, {})
    return OUTPUT


def main():
    if not INPUT_DIR.is_dir():
        raise SystemExit(f'REFUSING TO BUILD: source directory missing: {INPUT_DIR}')

    chapters = load_chapters(INPUT_DIR)

    # Zero reads as clean is the trap this repo's gates exist to avoid.
    if not chapters:
        raise SystemExit(f'REFUSING TO BUILD: no chapters matched {CHAPTER_GLOB} in {INPUT_DIR}')
    empty = [n for n, b in chapters if not b]
    if empty:
        raise SystemExit(f'REFUSING TO BUILD: chapters parsed with zero content: {empty}')

    total_words = 0
    total_breaks = 0
    for num, blocks in chapters:
        words = sum(len(v.split()) for k, v in blocks if k == 'p')
        breaks = sum(1 for k, _ in blocks if k == 'break')
        paras = sum(1 for k, _ in blocks if k == 'p')
        total_words += words
        total_breaks += breaks
        print(f'  Chapter {num:>2}: {paras:>3} paras, {breaks} breaks, ~{words} words')

    output = build_epub(chapters)
    print(f'\nChapters: {len(chapters)}')
    print(f'Scene breaks: {total_breaks}')
    print(f'Total: ~{total_words} words')
    print(f'EPUB written to: {output}')


if __name__ == '__main__':
    main()
