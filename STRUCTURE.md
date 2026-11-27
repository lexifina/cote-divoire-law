# Structure

| Folder | Contents |
| --- | --- |
| `constitution/` | Constitution du 8 novembre 2016 (loi n° 2016-886), révisée en 2020 : `preambule.md`, `art-001.md` … |
| `codes/<code>/` | Un code par dossier (`codes/code-penal/`, `codes/code-minier/`, `codes/code-forestier/` …) ; une loi postérieure instituant le même code en est une nouvelle version |
| `lois/<année>/<numéro>-<objet>/` | Lois (et lois organiques), par année de promulgation |
| `ordonnances/<année>/<numéro>-<objet>/` | Ordonnances |
| `decrets/<année>/<numéro>-<objet>/` | Décrets |
| `arretes/<année>/<numéro>-<objet>/` | Arrêtés (ministériels, interministériels) |
| `uemoa/<nature>/<année>/<numéro>-<objet>/` | Actes de l’UEMOA (`reglements/`, `actes-additionnels/`, `directives/` …), datés de leur entrée en vigueur |

Dans chaque dossier de texte : `README.md` (intitulé, source, date et son fondement, couche texte), `visas.md`, un
fichier par article (`art-001.md`, `art-002-bis.md` …), `signatures.md` ; `texte-integral.md` quand aucun article n'a
été repéré. Au plus 1 000 dossiers par répertoire. Les noms sont en français, la langue des textes.

`corpus.json` (`ci/national/acts`) énumère chaque texte : dossier, nature, numéro, date, intitulé, source.
