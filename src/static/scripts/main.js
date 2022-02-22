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


function myFunction() {
  var input, filter, products, div, h5, i, txtValue;
  input = document.getElementById("search-form");
  filter = input.value.toUpperCase();
  products = document.getElementById("products");
  div = products.getElementsByTagName("div");
  for (i = 0; i < div.length; i++) {
    h5 = div[i].getElementsByTagName("h5")[0];
    if (h5) {
      txtValue = h5.textContent || h5.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        div[i].style.display = "";
      } else {
        div[i].style.display = "none";
      }
    }
  }
}
