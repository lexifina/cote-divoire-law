"""The Constitution of 8 November 2016 (Loi n° 2016-886) and its revision by Loi constitutionnelle n° 2020-348.

Two born-digital sources with a text layer, both cached by fetch.py:
- AN_2016: the Assemblée nationale's PDF "Loi n° 2016-886 du 08 novembre 2016 portant Constitution", the text as
  promulgated (signed "Fait à Abidjan, le 08 novembre 2016").
- WIPO_2020: WIPO Lex record 22491, "Loi n° 2016-886 ... telle que modifiée par la loi constitutionnelle n°2020-348
  du 19 mars 2020" (author "Côte d'Ivoire"), which marks each article the 2020 law rewrote "Article N - Nouveau".

Version 2 (2020-03-19) is version 1 with every article marked "Nouveau" replaced by its WIPO text, credited to
Loi 2020-348 (the source's own marker). Every article not so marked is compared word for word with WIPO; those that
agree keep the 2016 wording (no change). Any that do not agree are listed by `report()` and handled in parse.py.
"""
from __future__ import annotations

import re
import unicodedata

from fetch import fetch
from pdftext import paragraphs

AN_2016 = ('https://www.assnat.ci/IMG/pdf/constitution_de_la_republique_de_cote_d_ivoireloi_-_no_2016-886_du_08_'
           'novembre_2016.pdf')
WIPO_2020 = ('https://wipolex-res.wipo.int/edocs/lexdocs/laws/fr/ci/ci023fr_1.pdf?last-modified=1773752329&Expires='
             '1793224426&Signature=P451hFRNMHwdF8sa3jTIFfjMInu0Hb5--7U9P5DbbEVowLv4mfTZ4iKsg4ox5MWvCYBYsZoOVZcjXLgf5DWj'
             '5xcUlVlzRCk~ZLz2DiMAEz1GjA-H0cpY4uKirMcgSEs-QjOCUHtmiiYULJ3SDiojoTwEim7KlXixVGG31EgGjXum5RDm4q95CYKp8jUE2'
             'yLllSRhgL3PCTAcGJWh5lxIkFYd3B82T9ldpozcn3kinaktzjEMKS8qHEqbFs~38WAyOcs50p70wkSerm7m1uZgbV~4m0kZR8zCZBzNQ'
             'gwBn931RHyyfs9RPcUs9QOWn7ccRhWUunI5ZqPq3Lh3xS1rmQ__&Key-Pair-Id=K1QGBX7Y6FHYJN')
WIPO_2020_STABLE = 'https://wipolex-res.wipo.int/edocs/lexdocs/laws/fr/ci/ci023fr_1.pdf'
WIPO_RECORD = 'https://www.wipo.int/wipolex/fr/legislation/details/22491'

HEADING = re.compile(r'^(TITRE|CHAPITRE|SECTION|PREAMBULE|PRÉAMBULE)\b', re.I)
END = re.compile(r'^Fait à Abidjan', re.I)


def words(s: str) -> list[str]:
    """Words for comparing two transcriptions: case, accents, punctuation and line-wrap hyphens ignored."""
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'(\w)- (\w)', r'\1\2', s)
    s = s.replace('-', '')
    return re.sub(r'[^\w]+', ' ', s).split()


def _hyphen_words(*texts: str) -> set[str]:
    """Words printed whole (not split at a line end) anywhere in the sources: a split "écono- mique" or a line-end
    "abso-" + "lue" is joined only if the whole word is printed somewhere."""
    out = set()
    for t in texts:
        out.update(w.lower() for w in re.findall(r'\w+', t))
    return out


def _structure(paras: list[tuple[str, bool]], marked: bool) -> tuple[str, dict[int, list[str]], dict[int, bool]]:
    """(preamble text, {article number: paragraphs}, {article number: marked "Nouveau"}). Title, chapter and
    section headings end the article before them and are not part of any article."""
    pre: list[str] = []
    arts: dict[int, list[str]] = {}
    new: dict[int, bool] = {}
    cur = None
    in_pre = False
    for text, bold in paras:
        if END.match(text):
            break
        if re.match(r'^PR[EÉ]AMBULE$', text, re.I):
            in_pre = True
            continue
        m = re.match(r'^Article\s+(\d+)\s*(-\s*Nouveau\s*)?\.?\s*(?:—\s*)?(.*)$', text, re.S)
        if m and (marked or not m.group(3)):
            cur = int(m.group(1))
            in_pre = False
            arts[cur] = [m.group(3).strip()] if m.group(3).strip() else []
            new[cur] = bool(m.group(2))
            continue
        if HEADING.match(text) or (bold and text.upper() == text and not text[:1].isdigit()):
            cur = None
            in_pre = False
            continue
        if in_pre:
            pre.append(text)
        elif cur is not None:
            arts[cur].append(text)
    return '\n'.join(pre), arts, new


def _join_spaced_hyphens(t: str, hw: set[str]) -> str:
    """WIPO's text keeps the Journal officiel's column hyphenation as "écono- mique": joined when the whole word is
    printed somewhere, otherwise read as a real hyphen ("lui- même" -> "lui-même")."""
    def rep(m):
        w = m.group(1) + m.group(2)
        return w if w.lower() in hw else m.group(1) + '-' + m.group(2)
    return re.sub(r'(\w+)- (\w+)', rep, t)


def load() -> dict:
    an_b, wi_b = fetch(AN_2016, offline=True), fetch(WIPO_2020, offline=True)
    raw_an = paragraphs(an_b, 'blocks')
    hw = _hyphen_words(*(t for t, _ in raw_an))
    raw_wi = paragraphs(wi_b, 'margin', hyphen_words=hw)
    raw_wi = [(_join_spaced_hyphens(t, hw), b) for t, b in raw_wi]
    pre16, a16, _ = _structure(raw_an, marked=False)
    pre20, a20, new20 = _structure(raw_wi, marked=True)
    return {'pre16': pre16, 'a16': a16, 'pre20': pre20, 'a20': a20, 'new20': new20,
            'an_bytes': an_b, 'wipo_bytes': wi_b}
