// JavaScript source code

var pages = 0;
var current_page = 0;

function onload(pages1, current_page1) {
    console.log("start")
    pages = pages1;
    current_page = current_page1;
    word = document.getElementById("temp").value;
    document.getElementById("textfield").value = word;
    if (pages != -1)
        document.getElementById("404").hidden = true;
    else
        document.getElementById("404").hidden = false;
}

function search() {
    word = document.getElementById("textfield").value;
    window.location.href ="/search?s=" + word+"&p=1";
}

function to_page() {

}