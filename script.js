const text = "WELCOME TO FD KHAN ACADEMY";

let index = 0;

function typeEffect(){

    const element = document.getElementById("typing-text");

    if(index < text.length){

        element.innerHTML += text.charAt(index);

        index++;

        setTimeout(typeEffect, 80);
    }
}

window.onload = typeEffect;
