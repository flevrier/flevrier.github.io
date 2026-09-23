import json
import os
import sys
from pathlib import Path

import requests

TOKEN = os.environ.get("ADS_TOKEN")
root = Path(__file__).resolve().parent.parent
output = root / "latest.json"

if not TOKEN:
    print("ADS_TOKEN is not set", file=sys.stderr)
    sys.exit(1)

query = {
    "q": 'author:"Levrier, F"',
    "fl": "title,author,year,abstract,bibcode,identifier",
    "rows": 1,
    "sort": "date desc",
}

r = requests.post(
    "https://api.adsabs.harvard.edu/v1/search/query",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json=query,
    timeout=30,
)
r.raise_for_status()
docs = r.json().get("response", {}).get("docs", [])

if not docs:
    print("No entry found from ADS", file=sys.stderr)
    sys.exit(1)

doc = docs[0]

# auteurs : decode + et al. si > 3 (meme convention que l'ancien script)
author_list = doc.get("author", [])
if len(author_list) > 3:
    authors = ", ".join(author_list[:3]) + " et al."
else:
    authors = ", ".join(author_list)

# lien arXiv (page abstract, comme l'ancien script)
arxiv = ""
for ident in doc.get("identifier", []):
    if ident.startswith("arXiv:"):
        arxiv = f"https://arxiv.org/abs/{ident[6:]}"
        break

latest = {
    "title": (doc.get("title") or [""])[0],
    "authors": authors,
    "year": str(doc.get("year", "")),
    "abstract": doc.get("abstract") or "",
    "ads": f"https://ui.adsabs.harvard.edu/abs/{doc['bibcode']}",
    "arxiv": arxiv,
    "pdf": "",
}

with open(output, "w") as f:
    json.dump(latest, f)

print("latest.json generated from ADS API")
