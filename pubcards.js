fetch("publications.json")
.then(r => r.json())
.then(data => {

data.sort((a,b) => b.year - a.year);

let html = "";

data.forEach(p => {

let absID = "abs_" + p.id;

html += `
<div class="pubcard">

<h3>${p.title}</h3>

<p class="pubauthors">${p.author} (${p.year})</p>

<div class="pubbuttons">

<button onclick="toggle('${absID}')">Abstract</button>

<a href="${p.adsurl}" target="_blank">ADS</a>

<a href="${p.bibtex}" target="_blank">BibTeX</a>

${p.pdf ? `<a href="${p.pdf}" target="_blank">PDF</a>` : ""}

</div>

<div id="${absID}" class="abstract" style="display:none;">
${p.abstract}
</div>

</div>
`;

});

document.getElementById("publist").innerHTML = html;

});

function toggle(id) {

let e = document.getElementById(id);

if(e.style.display=="none")
  e.style.display="block";
else
  e.style.display="none";

}