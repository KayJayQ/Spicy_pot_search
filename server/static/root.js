// JavaScript source code

function onload() {
    document.getElementById("textfield").value = "";
}

function submit() {
    text = document.getElementById("textfield").value;
    console.log(text);
    if (text != "")
        window.location.href = "/search?s=" + text + "&p=1";
}