const API_TOKEN = "diMsRZfYHkPv6jH66HmniHf88zxzoNiYN75qiNzW";

const url =
"https://api.adsabs.harvard.edu/v1/search/query?q=author:\"Levrier, F\"&fl=title,author,year,abstract,bibcode,identifier,links_data&rows=50";

fetch(url, {
  headers: {
    Authorization: "Bearer " + API_TOKEN
  }
})
.then(r => r.json())
.then(data => {

let html = "";

data.response.docs.forEach(p => {

let title = p.title ? p.title[0] : "";
let year = p.year || "";
let authors = p.author ? p.author.join(", ") : "";

let abstract = p.abstract || "";

if (abstract.length > 400)
  abstract = abstract.substring(0,400) + "...";

let adslink =
"https://ui.adsabs.harvard.edu/abs/" + p.bibcode;

let bibtexlink =
"https://ui.adsabs.harvard.edu/abs/" + p.bibcode + "/exportcitation";

let pdflink = "";

if (p.identifier) {
  let arxiv = p.identifier.find(x => x.startsWith("arXiv"));
  if (arxiv) {
    pdflink = "https://arxiv.org/pdf/" + arxiv.replace("arXiv:","");
  }
}

html += `
<div class="pub">

<h3>${title}</h3>

<p><i>${authors}</i> (${year})</p>

<p>${abstract}</p>

<p>
<a href="${adslink}" target="_blank">ADS</a> |
<a href="${bibtexlink}" target="_blank">BibTeX</a>
${pdflink ? '| <a href="'+pdflink+'" target="_blank">PDF</a>' : ''}
</p>

</div>
`;

});

document.getElementById("publist").innerHTML = html;

});