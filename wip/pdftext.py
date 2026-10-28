"""Paragraph text from born-digital PDFs (PyMuPDF text layer only; no OCR).

`paragraphs(pdf_bytes, mode)` returns the document as a list of paragraphs, in reading order, with page-number
lines dropped. Two layouts are handled:
- "blocks": each PDF text block is one paragraph (Word exports: the Assemblée nationale PDFs).
- "margin": one block per page holds many paragraphs; a paragraph ends where a line stops short of the right
  margin (justified text; the WIPO Lex consolidation printed from the Journal officiel layout).
"""
from __future__ import annotations

import re
import unicodedata

import fitz  # PyMuPDF

PAGE_NO = re.compile(r'^\s*\d{1,3}\s*$')


def clean(s: str) -> str:
    """Typesetting normalisation, applied once: NFC, NBSP and tabs to spaces, one apostrophe and quote form,
    runs of spaces collapsed."""
    s = unicodedata.normalize('NFC', s)
    s = s.replace(' ', ' ').replace(' ', ' ').replace('\t', ' ').replace('­', '')
    s = s.replace('’', '’').replace("'", '’').replace('‘', '’')
    s = s.replace('“', '«').replace('”', '»')
    s = re.sub(r'«\s*', '« ', s)
    s = re.sub(r'\s*»', ' »', s)
    s = re.sub(r'\s+([;:!?])', r' \1', s)          # French spacing before ; : ! ? (one space)
    s = re.sub(r'(\S)([;!?])', r'\1 \2', s)
    s = re.sub(r'\s+([.,])', r'\1', s)
    s = re.sub(r' {2,}', ' ', s)
    return s.strip()


def _lines(doc, page_filter=None):
    """(page index, block number, x0, x1, text) for every non-empty line."""
    for pi, page in enumerate(doc):
        for b in page.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                t = ''.join(s['text'] for s in ln['spans'])
                if t.strip():
                    bold = all(('Bold' in s['font'] or s['flags'] & 16) for s in ln['spans'] if s['text'].strip())
                    yield pi, b['number'], ln['bbox'][0], ln['bbox'][2], t, bold


def join_lines(lines: list[str], hyphen_words: set[str] | None = None) -> str:
    """Join wrapped lines into one paragraph. A line ending in a hyphen joins the next line without a space; the
    hyphen is dropped only when hyphen_words is given and the joined word without it is known there."""
    out = ''
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        if out.endswith('-') and ln[:1].islower() and hyphen_words is not None:
            head = re.search(r'(\w+)-$', out)
            tail = re.match(r'(\w+)', ln)
            if head and tail and (head.group(1) + tail.group(1)).lower() in hyphen_words:
                out = out[:-1] + ln
                continue
            out += ln
        elif out.endswith('-') and (ln[:1].isupper() or ln[:1].islower()):
            out += ln
        else:
            out = (out + ' ' + ln) if out else ln
    return out


def paragraphs(data: bytes, mode: str, hyphen_words: set[str] | None = None) -> list[tuple[str, bool]]:
    """[(paragraph text, is_bold)] for the whole document."""
    doc = fitz.open(stream=data, filetype='pdf')
    rows = [r for r in _lines(doc) if not PAGE_NO.match(r[4])]
    paras: list[tuple[list[str], bool]] = []
    if mode == 'blocks':
        key = None
        for pi, bn, x0, x1, t, bold in rows:
            if (pi, bn) != key:
                paras.append(([], bold))
                key = (pi, bn)
            paras[-1][0].append(t)
    else:
        right = {}
        for pi, bn, x0, x1, t, bold in rows:
            right[pi] = max(right.get(pi, 0), x1)
        open_ = False
        for pi, bn, x0, x1, t, bold in rows:
            starts_article = re.match(r'\s*Article\s+\d+', t) is not None
            if not open_ or starts_article:
                paras.append(([], bold))
            paras[-1][0].append(t)
            open_ = x1 >= right[pi] - 22
    return [(clean(join_lines(ls, hyphen_words)), b) for ls, b in paras if ''.join(ls).strip()]
