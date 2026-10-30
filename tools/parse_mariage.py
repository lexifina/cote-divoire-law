"""Builds scripts/cote-divoire-law/corpus.d/30-mariage.json from the cache only (no network).

    python -X utf8 scripts/cote-divoire-law/parse_mariage.py [--check]

Loi n° 2019-570 du 26 juin 2019 relative au mariage (the marriage title of the civil law). Words: the Assemblée
nationale's born-digital PDF of the law as adopted ("Loi relatif au mariage"). Number, promulgation and Journal officiel
date: the Journal officiel n° 10 spécial du 12 juillet 2019 (a scan with an OCR text layer, archived copy of the
Ministère de la Femme, de la Famille et de l'Enfant's PDF), used as a word-by-word witness only, as for the Code pénal
(parse_code_penal.py, whose helpers this reuses).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse_code_penal as P  # noqa: E402

AN_URL = 'https://www.assnat.ci/IMG/pdf/loi_relative_au_mariage.pdf'
AN_PAGE = 'https://www.assnat.ci/?loi-relatif-au-mariage'
JO_URL = 'http://www.famille.gouv.ci/public/documents/doc_drcc/loi_2019-570_sur_le_mariage.pdf'
JO_TS = '20200910165658'
JO_ARCHIVE = f'https://web.archive.org/web/{JO_TS}id_/{JO_URL}'
RETRIEVED = '2026-10-30'
PART = HERE / 'corpus.d' / '30-mariage.json'
LAST = 104          # the AN text ends at art. 104; the Journal officiel adds art. 105 (publication formula)

CORRECTIONS: list[tuple[str, str, str]] = [
    ('art-104', 'Le présent projet de loi abroge', 'La présente loi abroge'),
]
# Art. 105 is printed in the Journal officiel and missing from the AN text: taken from the gazette.
ART_105 = ('# Article 105\nLa présente loi sera publiée au Journal officiel de la République de Côte d’Ivoire et exécutée '
           'comme loi de l’Etat.\n')


def build() -> dict:
    units, plan = P.build_units(AN_URL, 'LOI RELATIF AU MARIAGE', LAST, CORRECTIONS)
    units['art-105'] = {'label': 'Article 105', 'kind': 'art', 'text': ART_105}
    return {'plan': {'label': 'Plan', 'kind': 'other', 'text': '# Plan\n' + '\n'.join(plan) + '\n'}, **units}


def main() -> None:
    units = build()
    if '--check' in sys.argv:
        jo = P.jo_text(JO_ARCHIVE, 'LA TENEUR SUIT', 'Fait à Abidjan, le 26 juin 2019')
        P.check({k: v for k, v in units.items() if k != 'plan'},
                units['plan']['text'].split('\n')[1:-1], jo, 'mariage_jo_diff.tsv')
    an_sha = hashlib.sha256(P.cached(AN_URL)).hexdigest()
    jo_sha = hashlib.sha256(P.cached(JO_ARCHIVE)).hexdigest()
    part = {
        'sources': [
            {'name': 'Assemblée nationale de Côte d’Ivoire: Loi relatif au mariage', 'url': AN_PAGE,
             'retrieved': RETRIEVED,
             'licence': 'Official text of the law. The site footer reads "Copyright ©2019 assnat.ci - Tous droits '
                        'resevés"; it states no licence for the legal texts it publishes.',
             'notes': f'PDF of the law as adopted, listed under "Lois" (born-digital, text layer), {AN_URL}, sha256 '
                      f'{an_sha}. It carries no number, date or signature.'},
            {'name': 'Journal officiel de la République de Côte d’Ivoire, n° 10 spécial du 12 juillet 2019',
             'url': JO_URL, 'retrieved': RETRIEVED,
             'licence': 'Official gazette of the Republic of Côte d’Ivoire, as published on the site of the '
                        'Ministère de la Femme, de la Famille et de l’Enfant; no licence stated.',
             'notes': f'Pages 253-259: "LOI n° 2019-570 du 26 juin 2019 relative au mariage", promulgation formula '
                      f'and "Fait à Abidjan, le 26 juin 2019. Alassane OUATTARA." A scanned issue with an OCR text '
                      f'layer, used for the number, the dates, art. 105 and as a word-by-word witness. Internet '
                      f'Archive copy {JO_TS}, sha256 {jo_sha}.'},
        ],
        'laws': {
            'loi-2019-570': {
                'label': 'Loi n° 2019-570',
                'title': 'Loi n° 2019-570 du 26 juin 2019 relative au mariage',
                'kind': 'law', 'enacted': '2019-06-26', 'published': '2019-07-12', 'url': JO_URL,
                'temporary_until': None, 'restores': None, 'note': None},
        },
        'acts': [{
            'slug': 'mariage',
            'short': 'Loi sur le mariage',
            'title': 'Loi n° 2019-570 du 26 juin 2019 relative au mariage',
            'url': AN_PAGE,
            'first_law': 'loi-2019-570',
            'earlier_laws': [],
            'versions': [{
                'from': '2019-07-12',
                'source_url': AN_URL,
                'sha256': an_sha,
                'units': units,
                'credits': {},
                'note': 'Text as adopted by the Assemblée nationale and promulgated on 26 June 2019; published in '
                        'the Journal officiel n° 10 spécial of 12 July 2019.',
            }],
        }],
        'decisions': [
            'Loi sur le mariage: the words are the Assemblée nationale\'s born-digital PDF of the law as adopted '
            '("Loi relatif au mariage", listed under "Lois"); number and dates come from the Journal officiel n° 10 '
            'spécial of 12 July 2019, pages 253-259 ("LOI n° 2019-570 du 26 juin 2019 relative au mariage", '
            'promulgation formula, "Fait à Abidjan, le 26 juin 2019"), a scan whose OCR text layer is used as a '
            'witness.',
            'Loi sur le mariage: the AN text was aligned word by word (letters and figures, accents and case '
            'ignored) with the Journal officiel text layer and every differing stretch was looked up on the gazette '
            'page. Apart from headings and OCR misreadings, the promulgated text differs in two places, and the '
            'gazette is followed: art. 104 opens "La présente loi abroge" (AN "Le présent projet de loi abroge"), '
            'and art. 105 (publication in the Journal officiel and execution as a law of the State), which the AN '
            'text lacks, is taken from the gazette.',
            'Loi sur le mariage: dated 12 July 2019, the day of its Journal officiel issue; art. 105 orders it '
            '"publiée au Journal officiel … et exécutée comme loi de l’Etat" and the law sets no other date.',
            'Loi sur le mariage: one version, the law as enacted; no amendment was looked for or applied. Headings '
            'are in the act\'s "plan" file as the AN prints them (the gazette numbers chapters and sections in Arabic '
            'figures); unit rules as for the Code pénal.',
        ],
        'ai_use': ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code, chose the sources and "
                   'wrote the decisions. No model wrote, summarised or transformed legal text: the text is taken '
                   'from the official PDFs by deterministic code.'],
    }
    PART.parent.mkdir(exist_ok=True)
    tmp = PART.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, PART)
    print(f'{PART.name}: {len(units)} units')


if __name__ == '__main__':
    main()
