#!/usr/bin/env python3
"""Build Book 1 EPUB from manuscript text file."""

import re
import html
from ebooklib import epub

INPUT = '/workspaces/gosquad/6_manuscript/book_1/book1_manuscript.txt'
OUTPUT = '/workspaces/gosquad/6_manuscript/book_1/GoSquad_Book1.epub'

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


def load_manuscript(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def split_chapters(text):
    """Split manuscript into chapters using the header pattern."""
    # Pattern: "Vaughn / Go Squad / PAGE Chapter N"
    pattern = r'Vaughn / Go Squad / \d+ Chapter (\d+) '
    splits = list(re.finditer(pattern, text))

    chapters = []
    for i, match in enumerate(splits):
        ch_num = int(match.group(1))
        # Content starts after the header
        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
        content = text[start:end].strip()
        # Remove trailing manuscript headers (orphan "Vaughn / Go Squad / N" lines)
        content = re.sub(r'\s*Vaughn / Go Squad / \d+\s*$', '', content)
        chapters.append((ch_num, content))

    return chapters


def text_to_html(text):
    """Convert plain text paragraphs to HTML."""
    # The manuscript uses double-newlines or single-newlines for paragraph breaks
    text = html.escape(text)

    # Normalize line breaks - split on double newlines first
    paragraphs = re.split(r'\n\s*\n', text)

    html_parts = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # Check for scene breaks (lines that are just whitespace or dashes/asterisks)
        if re.match(r'^[\s\-\*#=]+$', para):
            html_parts.append('<p class="scene-break">* * *</p>')
        else:
            # Within a paragraph, replace single newlines with spaces
            para = re.sub(r'\s*\n\s*', ' ', para)
            # Clean up multiple spaces
            para = re.sub(r' {2,}', ' ', para)
            html_parts.append(f'<p>{para}</p>')

    return '\n'.join(html_parts)


def build_epub(chapters):
    book = epub.EpubBook()

    # Metadata
    book.set_identifier('gosquad-book1-arc')
    book.set_title(TITLE)
    book.set_language(LANG)
    book.add_author(AUTHOR)
    book.add_metadata('DC', 'description',
                      'Advanced Reader Copy — Not for distribution')

    # CSS
    style = epub.EpubItem(
        uid='style',
        file_name='style/default.css',
        media_type='text/css',
        content=CSS.encode('utf-8')
    )
    book.add_item(style)

    # Title page
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

    # Chapters
    epub_chapters = [title_page]
    toc = []

    for ch_num, content in chapters:
        ch_title = f'Chapter {ch_num}'
        ch = epub.EpubHtml(
            title=ch_title,
            file_name=f'chapter_{ch_num:02d}.xhtml',
            lang=LANG
        )
        body_html = text_to_html(content)
        ch.content = f'''<html><head><link rel="stylesheet" href="style/default.css"/></head>
<body>
<h1>{ch_title}</h1>
{body_html}
</body></html>'''.encode('utf-8')
        ch.add_item(style)
        book.add_item(ch)
        epub_chapters.append(ch)
        toc.append(ch)

    # Table of contents
    book.toc = toc

    # Navigation
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Spine
    book.spine = ['nav'] + epub_chapters

    epub.write_epub(OUTPUT, book, {})
    return OUTPUT


def main():
    text = load_manuscript(INPUT)
    chapters = split_chapters(text)
    print(f'Found {len(chapters)} chapters')
    for ch_num, content in chapters:
        words = len(content.split())
        print(f'  Chapter {ch_num}: ~{words} words')
    output = build_epub(chapters)
    total_words = sum(len(c.split()) for _, c in chapters)
    print(f'\nTotal: ~{total_words} words')
    print(f'EPUB written to: {output}')


if __name__ == '__main__':
    main()
