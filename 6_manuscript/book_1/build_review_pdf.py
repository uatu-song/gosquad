#!/usr/bin/env python3
"""Render GoSquad_Book1_REVIEW.epub to a PDF (same text, same version stamp).

Reads the epub directly so the PDF can never drift from the shipped artifact.
Output: GoSquad_Book1_REVIEW.pdf next to the epub.

    python3 build_review_pdf.py
"""
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate, Spacer)

HERE = Path(__file__).resolve().parent
EPUB = HERE / "GoSquad_Book1_REVIEW.epub"
OUT = HERE / "GoSquad_Book1_REVIEW.pdf"
VERSION = (HERE / "REVIEW_VERSION").read_text().strip()

FONT = "Times-Roman"
BODY = ParagraphStyle("body", fontName=FONT, fontSize=11.5, leading=16,
                      firstLineIndent=0.3 * inch, alignment=TA_JUSTIFY)
FIRST = ParagraphStyle("first", parent=BODY, firstLineIndent=0)
BREAK = ParagraphStyle("break", parent=BODY, firstLineIndent=0,
                       alignment=TA_CENTER, spaceBefore=12, spaceAfter=12)
HEAD = ParagraphStyle("head", fontName=FONT, fontSize=15, leading=20,
                      alignment=TA_CENTER, spaceBefore=110, spaceAfter=40)
TITLE = ParagraphStyle("title", fontName=FONT, fontSize=28, leading=34,
                       alignment=TA_CENTER, spaceBefore=200, spaceAfter=18)
BYLINE = ParagraphStyle("byline", fontName="Times-Italic", fontSize=14,
                        leading=18, alignment=TA_CENTER, spaceAfter=60)
SERIES = ParagraphStyle("series", fontName=FONT, fontSize=11, leading=14,
                        alignment=TA_CENTER)
NOTE = ParagraphStyle("note", fontName=FONT, fontSize=10.5, leading=16,
                      alignment=TA_LEFT, spaceAfter=12)
NOTE_H = ParagraphStyle("noteh", parent=NOTE, alignment=TA_CENTER,
                        spaceBefore=120, spaceAfter=28)
STAMP = ParagraphStyle("stamp", parent=NOTE, fontSize=9, textColor="#666666",
                       spaceBefore=30)


class Blocks(HTMLParser):
    """Collect (tag, class, inner-markup) for h1/h2/p; keep <i>/<b> inline."""

    def __init__(self):
        super().__init__()
        self.blocks, self.cur, self.cls, self.buf = [], None, None, []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "p"):
            self.cur, self.cls, self.buf = tag, dict(attrs).get("class", ""), []
        elif tag in ("i", "b", "em", "strong") and self.cur:
            self.buf.append("<i>" if tag in ("i", "em") else "<b>")
        elif tag == "br" and self.cur:
            self.buf.append("<br/>")

    def handle_endtag(self, tag):
        if tag == self.cur:
            self.blocks.append((tag, self.cls, "".join(self.buf).strip()))
            self.cur = None
        elif tag in ("i", "em") and self.cur:
            self.buf.append("</i>")
        elif tag in ("b", "strong") and self.cur:
            self.buf.append("</b>")

    def handle_data(self, data):
        if self.cur:
            self.buf.append(data.replace("&", "&amp;").replace("<", "&lt;"))


def blocks_of(z, name):
    p = Blocks()
    p.feed(z.read(name).decode("utf-8"))
    return p.blocks


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 9)
    canvas.drawCentredString(letter[0] / 2, 0.6 * inch, str(doc.page))
    canvas.setFillColor("#888888")
    canvas.drawString(inch, 0.6 * inch, f"Go Squad · Book 1 · Review copy v{VERSION}")
    canvas.restoreState()


def main():
    z = zipfile.ZipFile(EPUB)
    opf = z.read("EPUB/content.opf").decode()
    ids = re.findall(r'<itemref idref="([^"]+)"', opf)
    hrefs = {m.group(2): m.group(1) for m in
             re.finditer(r'<item href="([^"]+)" id="([^"]+)"', opf)}
    story = []
    for ref in ids:
        name = "EPUB/" + hrefs[ref]
        if name.endswith("nav.xhtml"):
            continue
        if story:
            story.append(PageBreak())
        for tag, cls, text in blocks_of(z, name):
            if name.endswith("title.xhtml"):
                st = {"h1": TITLE, "p": BYLINE if cls == "byline" else SERIES}[tag]
            elif name.endswith("notice.xhtml"):
                st = NOTE_H if tag == "h2" else STAMP if cls == "stamp" else NOTE
            elif tag == "h1":
                st = HEAD
            else:
                st = {"first": FIRST, "scene-break": BREAK}.get(cls, BODY)
            story.append(Paragraph(text, st))
    doc = SimpleDocTemplate(str(OUT), pagesize=letter, leftMargin=inch,
                            rightMargin=inch, topMargin=inch, bottomMargin=inch,
                            title="Go Squad — Book One (Review copy v%s)" % VERSION,
                            author="J. S. Vaughn")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
