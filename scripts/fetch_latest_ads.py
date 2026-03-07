import requests
import json
import os

TOKEN = os.environ.get("ADS_TOKEN")

query = {
  "q": "author:\"Levrier, F\"",
  "fl": "title,author,year,abstract,bibcode,identifier",
  "rows": 1,
  "sort": "date desc"
}

r = requests.post(
    "https://api.adsabs.harvard.edu/v1/search/query",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json=query
)

data = r.json()
doc = data["response"]["docs"][0]

latest = {
  "title": doc.get("title", [""])[0],
  "authors": doc.get("author", []),
  "year": doc.get("year"),
  "abstract": doc.get("abstract", ""),
  "adsurl": f"https://ui.adsabs.harvard.edu/abs/{doc['bibcode']}",
  "pdf": ""
}

# PDF (souvent arXiv)
if "identifier" in doc:
    for ident in doc["identifier"]:
        if ident.startswith("arXiv:"):
            latest["pdf"] = f"https://arxiv.org/pdf/{ident[6:]}.pdf"

with open("latest.json", "w") as f:
    json.dump(latest, f)