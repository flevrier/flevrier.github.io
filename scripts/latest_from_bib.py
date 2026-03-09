import bibtexparser
import json
from pathlib import Path
from pylatexenc.latex2text import LatexNodes2Text

root = Path(__file__).resolve().parent.parent
bibfile = root / "Levrier-publications.bib"
output = root / "latest.json"

with open(bibfile) as f:
    bib = bibtexparser.load(f)

entries = sorted(
    bib.entries,
    key=lambda e: int(e.get("year", 0)),
    reverse=True
)

if not entries:
    print("No entry found")
    exit(1)

e = entries[0]

def latex_to_text(s):
    if not s:
        return ""
    return LatexNodes2Text().latex_to_text(s)

def get(field):
    return latex_to_text(e.get(field, "")).strip()

# auteurs : décodage + et al. si > 3
authors_raw = e.get("author", "")
authors_list = [latex_to_text(a.strip()) for a in authors_raw.split(" and ")]

if len(authors_list) > 3:
    authors = ", ".join(authors_list[:3]) + " et al."
else:
    authors = ", ".join(authors_list)

latest = {
    "title": get("title"),
    "authors": authors,
    "year": get("year"),
    "abstract": get("abstract"),
    "ads": e.get("adsurl", ""),
    "arxiv": e.get("eprint") and f"https://arxiv.org/abs/{e.get('eprint')}",
    "pdf": e.get("url", "")
}

with open(output, "w") as f:
    json.dump(latest, f)

print("latest.json generated")