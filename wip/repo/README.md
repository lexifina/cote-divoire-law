# Côte d’Ivoire: law history in git

The law of Côte d’Ivoire as a git history. Each provision is one file, each law gets one commit on the day it took effect, and the law that made each change is the commit's author. `git blame` names the law behind every paragraph, `git log` lists every change to an article, and `tools/en_vigueur_au.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `ci/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution de la République de Côte d’Ivoire (loi n° 2016-886 du 8 novembre 2016) | 2 | As promulgated, in force 8 November 2016; revised by Loi constitutionnelle n° 2020-348, in force 19 March 2020 (26 articles) |

The per-act `README.md` in each folder lists every provision, how often it changed and when.

**Why only the Constitution, and only two versions.** The Journal officiel (sgg.gouv.ci) was unreachable from our machine and is not consolidated, and no official site publishes dated versions of the codes. The Constitution has two official texts with a text layer: the Assemblée nationale's PDF of the 2016 text, and WIPO Lex's consolidation as amended in 2020, which marks every article the 2020 law rewrote "Nouveau". WIPO Lex lists that 2020 consolidation as its most recent version ("Version la plus récente dans WIPO Lex"). The Code pénal of 2019 is not included yet because its in-force date is not sourced; the data protection law (Loi n° 2013-450) is published only as an image scan, which this record does not transcribe.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 55 say on 1 January 2019? | `python tools/en_vigueur_au.py 2019-01-01 constitution 55` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2019-01-01T23:59:59Z" main -- constitution/art-055.md):constitution/art-055.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2019-01-01T23:59:59Z" main -- constitution/art-055.md; git show "$($r):constitution/art-055.md"` |
| Which law wrote each paragraph of art. 55? | `git blame constitution/art-055.md` |
| Every change to an article, word by word | `git log -p --word-diff constitution/art-055.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/lc-2020-348` (tags `law/<key>` mark each law's commit) |
| The whole Constitution on a date | `python tools/en_vigueur_au.py 2017-01-01 constitution` |
| Which law gave a provision its wording on a date | `python tools/en_vigueur_au.py --law 2021-01-01 constitution 177` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Africa/Abidjan (UTC), on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read; the promulgation date is the `Enacted:` trailer.
- **The Constitution fixes its own entry into force** (art. 184): "La présente Constitution entre en vigueur à compter du jour de sa promulgation par le Président de la République". So the 2016 text is dated 8 November 2016, its promulgation ("Fait à Abidjan, le 08 novembre 2016").
- **The 2020 revision is dated 19 March 2020**, the promulgation of Loi constitutionnelle n° 2020-348: WIPO Lex gives "Modifié jusqu’à: 19 mars 2020" and its consolidated text is signed "Fait à Abidjan, le 19 mars 2020". The Journal officiel text of that law, with any entry-into-force clause of its own, was not found.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- **Against the 2020 consolidation:** today's text is word for word WIPO Lex's consolidated text, headings aside, except four typesetting slips in WIPO's copy of articles the 2020 law did not touch and one in art. 177 ("Journal official"), where the 2016 wording is kept. Each is listed in REPRODUCE.md.
- **Against the 2016 text:** every article WIPO does not mark "Nouveau" was compared word for word with the Assemblée nationale's 2016 text, and all agree apart from those slips. So the 2020 law changed exactly the marked articles.
- **Nothing dropped:** every word of the body of both PDFs, from the preamble to the signature, is in a provision file except the title, chapter and section headings.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **The first commit** is the Constitution as promulgated, credited to Loi n° 2016-886.
- **The 2020 commit** holds exactly the articles WIPO Lex marks "Nouveau", credited to Loi constitutionnelle n° 2020-348. Two of them (arts. 148 and 149) are marked "Nouveau" but read word for word as in 2016; the commit names them in its `Also-concerns:` trailer.
- Blame credits whole lines (one paragraph per line). Within a rewritten article, a paragraph whose words did not change keeps its 2016 line, so blame names 2016 for it. Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **Only the Constitution of 2016.** Earlier constitutions (1960, 2000) are not in this record.
- **Headings** (Titre, Chapitre, Section) are left out; each file starts with "# Article N". The preamble is one file. The promulgation formula and signature lines are left out.
- **Publication dates.** The Journal officiel was not available, so laws carry their promulgation date only.
- **No OCR.** Texts published only as scanned images are not included.

## How it is built

`tools/fetch.py` downloads each source once with curl, at no more than one request per second per host, cached by the sha256 of its URL; WIPO serves its PDF only through a signed link printed on the record page, so fetch.py reads that page and then the link. `tools/parse.py` reads only the cache: `tools/pdftext.py` turns the PDFs' text layer into paragraphs, `tools/constitution.py` splits them into articles, finds WIPO's "Nouveau" marks and compares every article, and parse.py writes `corpus.json`; the shared builder `tools/build.py` turns that into the commits. `REPRODUCE.md` lists every source, command, tool version and decision, and the result of the hash-for-hash rebuild.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Assemblée nationale](https://www.assnat.ci/?-la-constitution-) | PDF of Loi n° 2016-886 portant Constitution, the text as promulgated (text layer) | Version 1 |
| [WIPO Lex, record CI023](https://www.wipo.int/wipolex/fr/legislation/details/22491) | The Constitution as amended by Loi constitutionnelle n° 2020-348, every rewritten article marked "Nouveau"; PDF (text layer) and an HTML rendering | Version 2, its date and its credits |
| [Journal officiel (SGG)](https://www.sgg.gouv.ci) | The official gazette, not consolidated | Not reachable from our machine; the Internet Archive holds only older laws |
| [Conseil constitutionnel](https://www.conseil-constitutionnel.ci/lois-et-decrets/la-constitution) | A Word export of the 2016 text (May 2017) | Not used: it differs from both texts above in 16 articles and looks like a pre-adoption draft |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

See [LICENSE](LICENSE). Texts: Assemblée nationale de Côte d’Ivoire (https://www.assnat.ci) and WIPO Lex (https://www.wipo.int/wipolex), official texts of the Republic of Côte d’Ivoire, reproduced with that attribution. Lexifina's arrangement, messages, tables and tools are CC0.

This repository is not legal advice.

## En français

Ce dépôt retrace l’histoire de la Constitution ivoirienne du 8 novembre 2016 dans git : un fichier par article, un commit par loi à la date de son entrée en vigueur, et la loi qui a modifié le texte comme auteur du commit. Il contient deux versions : le texte promulgué le 8 novembre 2016 (PDF de l’Assemblée nationale) et le texte révisé par la loi constitutionnelle n° 2020-348 du 19 mars 2020 (consolidation de WIPO Lex, où les 26 articles réécrits portent la mention « Nouveau »). `python tools/en_vigueur_au.py 2019-01-01 constitution 55` affiche l’article 55 tel qu’il était en vigueur à cette date, et `git blame constitution/art-055.md` nomme la loi à l’origine de chaque alinéa. Ce dépôt ne constitue pas un avis juridique.
