import bibtexparser
import json
from pathlib import Path

# Chemins
root = Path(__file__).resolve().parent.parent
bibfile = root / "Levrier-publications.bib"
output = root / "latest.json"

# Charger le BibTeX
with open(bibfile) as f:
    bib = bibtexparser.load(f)

# Trier par année (le plus récent d’abord)
entries = sorted(
    bib.entries,
    key=lambda e: int(e.get("year", 0)),
    reverse=True
)

if not entries:
    print("No entry found")
    exit(1)

e = entries[0]

def get(field):
    return e.get(field, "")

latest = {
    "title": get("title"),
    "authors": get("author"),
    "year": get("year"),
    "abstract": get("abstract"),
    "ads": get("adsurl"),
    "arxiv": get("eprint") and f"https://arxiv.org/abs/{get('eprint')}",
    "pdf": get("url") or ""
}

# Écrire latest.json à la racine
with open(output, "w") as f:
    json.dump(latest, f)

print("latest.json generated at", output)