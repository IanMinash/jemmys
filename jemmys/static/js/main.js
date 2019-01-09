var productPhotos = document.querySelectorAll(".product .prod-photo");

function toggleNav(){
  document.querySelector('.side-nav-bg').classList.toggle("dismissed");
}

document.querySelector('#show-nav').addEventListener("click", toggleNav);
document.querySelector('#dismiss-nav').addEventListener("click", toggleNav);

function toggleImage() {
  images = this.querySelectorAll("img");
  images.forEach(function(image) {
    image.classList.toggle("d-none");
  });
}

function oneToOne() {
  productPhotos.forEach(function(product) {
    if (Math.abs(product.offsetHeight - product.offsetWidth) > 2) {
      product.style.height = product.offsetWidth + 'px';
    }
  });
}

var GETform = document.querySelector('#call_page');

function categoryRequest() {
  document.querySelector('#get_param').setAttribute('name', 'category');
  document.querySelector('#get_param').setAttribute('value', this.innerHTML);
  GETform.submit();
}

productPhotos.forEach(function(product) {
  product.addEventListener("mouseover", toggleImage);
  product.addEventListener("mouseout", toggleImage);
});

window.addEventListener("load", oneToOne);
window.addEventListener("resize", oneToOne);

