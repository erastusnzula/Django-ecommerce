function init(){
}
function changeImage(event){
    var mainImage  = document.getElementById('mainImage')
    mainImage.src= event.target.src
}
window.onload = init;

function getFooter(){
    'use strict'
    if (document && document.getElementById){
        const footerEnd = document.getElementById('footer');
        footerEnd.innerHTML = "Copyright &copy " + new Date().getFullYear();
    }
}
getFooter()