fetch("files/quotes.txt")
.then(response => response.text())
.then(text => {

let quotes = text.split("\n\n");

let q = quotes[Math.floor(Math.random()*quotes.length)];

document.getElementById("quote").innerHTML = <em>q</em>;

});