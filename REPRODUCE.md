# How this repository was made (Côte d’Ivoire)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Assemblée nationale de Côte d’Ivoire | <https://www.assnat.ci/?-la-constitution-> | 2026-10-28 | Official text of the law. The site footer reads "Copyright ©2019 assnat.ci - Tous droits resevés"; it states no licence for the legal texts it publishes. |
| WIPO Lex (World Intellectual Property Organization) | <https://www.wipo.int/wipolex/fr/legislation/details/22491> | 2026-10-28 | WIPO Lex reproduces national legislation for information; the text is the official text of Côte d’Ivoire. WIPO's general terms of use apply to the site. |
| Other sites consulted | <https://www.assnat.ci> | 2026-10-28 | n/a |
| Assemblée nationale de Côte d’Ivoire: Loi portant Code pénal | <https://www.assnat.ci/?loi-portant-code-penal> | 2026-10-30 | Official text of the law. The site footer reads "Copyright ©2019 assnat.ci - Tous droits resevés"; it states no licence for the legal texts it publishes. |
| Journal officiel de la République de Côte d’Ivoire, n° 9 spécial du 10 juillet 2019 | <https://www.famille.gouv.ci/public/documents/doc_drcc/loi_2019-574_portant_code_p%C3%A9nal.pdf> | 2026-10-30 | Official gazette of the Republic of Côte d’Ivoire, as published on the site of the Ministère de la Femme, de la Famille et de l’Enfant; no licence stated. |
| Assemblée nationale de Côte d’Ivoire: Loi relatif au mariage | <https://www.assnat.ci/?loi-relatif-au-mariage> | 2026-10-30 | Official text of the law. The site footer reads "Copyright ©2019 assnat.ci - Tous droits resevés"; it states no licence for the legal texts it publishes. |
| Journal officiel de la République de Côte d’Ivoire, n° 10 spécial du 12 juillet 2019 | <http://www.famille.gouv.ci/public/documents/doc_drcc/loi_2019-570_sur_le_mariage.pdf> | 2026-10-30 | Official gazette of the Republic of Côte d’Ivoire, as published on the site of the Ministère de la Femme, de la Famille et de l’Enfant; no licence stated. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution de la République de Côte d’Ivoire (loi n° 2016-886 du 8 novembre 2016) | 2 | 2016-11-08 to 2020-03-19 |
| `code-penal` | Code pénal (Loi n° 2019-574 du 26 juin 2019) | 1 | 2019-07-10 to 2019-07-10 |
| `mariage` | Loi n° 2019-570 du 26 juin 2019 relative au mariage | 1 | 2019-07-12 to 2019-07-12 |

The build made 4 commits:

| Commits | Kind |
| ---: | --- |
| 3 | first version of an act |
| 1 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futur`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 4 laws in the record.
- 8 tags.

## Dates

Each commit is dated at noon (Africa/Abidjan) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Not applied as a general rule. The Constitution fixes its own entry into force, art. 184: "La présente Constitution entre en vigueur à compter du jour de sa promulgation par le Président de la République"; each version is dated by the promulgation of the law that made it. https://www.assnat.ci/IMG/pdf/constitution_de_la_republique_de_cote_d_ivoireloi_-_no_2016-886_du_08_novembre_2016.pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `654bcb8809286c77c927ed1b907e86fc8ecf29583555c3df62e08b69aed969c7` (561440 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

4 versions of 3 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 4 history commits and 8 tags (history tip `673c29ad0b5873efb3789f6f9f49621426a3c367`).

## Decisions made by hand

- Acts: the Constitution here; the Code pénal of 2019 is a separate part (its decisions are listed under "Code pénal"). Loi n° 2013-450 (data protection) is published by ARTCI only as an image scan: left out (no OCR).
- Version 1 (2016-11-08) is the Assemblée nationale PDF of Loi n° 2016-886, signed "Fait à Abidjan, le 08 novembre 2016", dated by art. 184 (in force from promulgation) and credited to that law as enacted.
- The Conseil constitutionnel's constitution_2016.pdf (Word 2010, May 2017) differs from both the Assemblée nationale and WIPO texts in 16 articles (2, 21, 27, 31, 33, 78-81, 87, 90, 93, 117, 135, 147, 175), and the Assemblée nationale text agrees with WIPO on all of them, so it looks like a pre-adoption draft and is not used.
- Version 2 (2020-03-19) is dated by the promulgation of Loi constitutionnelle n° 2020-348: WIPO Lex gives "Modifié jusqu’à: 19 mars 2020" and its consolidated text is signed "Fait à Abidjan, le 19 mars 2020". The Journal officiel text of the 2020 law itself, with any entry-into-force clause of its own, was not found; art. 184 (unchanged) puts the Constitution in force on promulgation.
- Credits for version 2 come only from WIPO's own "Nouveau" markers: articles 55, 56, 57, 59, 62, 74, 78, 79, 90, 94, 101, 109, 134, 137, 143, 144, 146, 147, 148, 149, 150, 151, 160, 177, 181, 182 (26 articles) are credited to Loi constitutionnelle n° 2020-348. Of these, 24 changed words; articles 148, 149 are marked "Nouveau" but read word for word as in 2016, so they are credited without a change of wording. WIPO also marks the heading "CHAPITRE 4 NOUVEAU"; headings are not units.
- Every article not marked "Nouveau" was compared word for word (case, accents, punctuation and line-break hyphens ignored) with the 2016 text: all agree, except WIPO typesetting slips in articles 26 (WIPO prints "dévelop pement"); 51 (WIPO prints "présidentielles" for "présidentielle"); 97 (WIPO prints "huis clos" / "compterendu" for "huis-clos" / "compte rendu"); 125 (WIPO prints "environnementet" for "environnement et"); 152 (WIPO prints "béné ficiant"). Those keep the 2016 wording. The preamble agrees too.
- Within a "Nouveau" article, a paragraph whose words equal a 2016 paragraph of the same article keeps the 2016 typesetting (apostrophes, accents on capitals), so only reworded paragraphs show as changed lines.
- WIPO's PDF reflows the text and runs some paragraphs together (in 10 unchanged articles it merges two 2016 paragraphs). A "Nouveau" article's paragraph is split after a sentence end where the 2016 text or WIPO's HTML rendering of the same record breaks a paragraph at exactly that point (6 words either side): art. 56 (last paragraph, "La convocation des électeurs…", as in 2016) and art. 137 (third paragraph, "Une disposition déclarée inconstitutionnelle…", as in the HTML).
- Art. 177, last paragraph: WIPO prints "Journal official" (in both its PDF and HTML); the paragraph is otherwise word for word the 2016 paragraph, which reads "Journal officiel", so "officiel" is kept.
- WIPO's HTML drops spaces between some words ("cettefin", "dela", "auxlois", "leurconformite" in arts. 62, 134, 177, 181), so it is never the source of words.
- Two fixes to the 2016 parse: art. 165 shares a PDF text block with the heading line before it ("DE LA REPUBLIQUE Article 165") and is split off; WIPO spaces out its preamble heading ("P R É A M B U L E").
- Typesetting is normalised once: NBSP to space, one apostrophe (’) and one quotation form (« »), French spacing before ; : ! ?, list markers (-, •, the Symbol-font bullet) to "— ", column hyphenation joined only where the whole word is printed somewhere in the sources. The Assemblée nationale PDF breaks list items across text blocks; a block that does not end in . ; : ! ? » runs on into the next, and items are split at "; -".
- Title, chapter and section headings are not units; each file starts with "# Article N". The preamble is one unit. The promulgation formula and the signature lines are left out.
- All dates are promulgation dates; the Journal officiel publication dates were not available, so `published` is empty.
- Code pénal: the words are the Assemblée nationale's born-digital PDF of the law as adopted ("Loi portant Code pénal", listed under "Lois"). Its number and dates come from the Journal officiel n° 9 spécial of 10 July 2019, pages 201-252, which prints "LOI n° 2019-574 portant Code pénal", the promulgation formula and "Fait à Abidjan, le 26 juin 2019"; that issue is a scan whose OCR layer is not used for words.
- Code pénal: the AN text was aligned word by word (letters and numbers, accents and case ignored) with the Journal officiel OCR layer, from the promulgation formula to the signature, and every differing stretch was looked up on the gazette page. Apart from headings and OCR misreadings ("l" for "1", "IO" for "10", split words), the promulgated text differs from the adopted text in five places, and the Journal officiel wording is used there: art. 101 "écarté autrement que l’auteur" (AN "autrement et que"); art. 154 "sections 1 et 2" (AN "sections I et II"); art. 255 "Au sens de la présente loi" (AN "Au sens du présent projet de loi"); art. 308 third item numbered "3°" (AN repeats "2°"); art. 362 "des personnes dont ont exploité" (AN "dont ils ont exploité"). Arts. 101 and 362 are kept as printed in the gazette although they read as slips.
- Code pénal: the headings in the "plan" file are the AN's; the Journal officiel numbers some chapters and sections in Arabic figures ("CHAPITRE 3", "Section 10") where the AN uses Roman ones.
- Code pénal: dated 10 July 2019, the day of its Journal officiel issue. Art. 565 orders the law "publiée au Journal officiel de la République de Côte d’Ivoire et exécutée comme loi de l’Etat" and the law sets no other date; the Constitution's promulgation rule (art. 184) is the Constitution's own and is not applied to it. No general rule adding a delay after publication was found.
- Code pénal: the record holds the Code as enacted. It has since been amended (among others by Loi n° 2021-893 du 21 décembre 2021); those amending laws were not found as text-layer official texts, so they are not applied and today's text may differ.
- Code pénal: article labels ("Article 1 :") become "# Article N"; Livre, Titre, Chapitre and Section headings go to the act's "plan" file, each with the article it precedes; the title line is left out. A text block that does not end a sentence is joined to the next unless that one is a heading, an article or a list item (page and column breaks); a heading printed on two lines is joined; numbered items run into one block ("… ; 2° …") each start a line. List numbers are spaced "1° crime" (the AN PDF prints "1°crime", the gazette "1 ° crime").
- Loi sur le mariage: the words are the Assemblée nationale's born-digital PDF of the law as adopted ("Loi relatif au mariage", listed under "Lois"); number and dates come from the Journal officiel n° 10 spécial of 12 July 2019, pages 253-259 ("LOI n° 2019-570 du 26 juin 2019 relative au mariage", promulgation formula, "Fait à Abidjan, le 26 juin 2019"), a scan whose OCR text layer is used as a witness.
- Loi sur le mariage: the AN text was aligned word by word (letters and figures, accents and case ignored) with the Journal officiel text layer and every differing stretch was looked up on the gazette page. Apart from headings and OCR misreadings, the promulgated text differs in two places, and the gazette is followed: art. 104 opens "La présente loi abroge" (AN "Le présent projet de loi abroge"), and art. 105 (publication in the Journal officiel and execution as a law of the State), which the AN text lacks, is taken from the gazette.
- Loi sur le mariage: dated 12 July 2019, the day of its Journal officiel issue; art. 105 orders it "publiée au Journal officiel … et exécutée comme loi de l’Etat" and the law sets no other date.
- Loi sur le mariage: one version, the law as enacted; no amendment was looked for or applied. Headings are in the act's "plan" file as the AN prints them (the gazette numbers chapters and sections in Arabic figures); unit rules as for the Code pénal.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code, chose the sources and wrote the decisions. No model wrote, summarised or transformed legal text: the text is taken from the official PDFs by deterministic code.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code, chose the sources and wrote the decisions. No model wrote, summarised or transformed legal text: the text is taken from the official PDF by deterministic code.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code, chose the sources and wrote the decisions. No model wrote, summarised or transformed legal text: the text is taken from the official PDFs by deterministic code.
