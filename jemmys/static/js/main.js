var productPhotos = document.querySelectorAll(".product .prod-photo");
var images;

function toggleImage() {
  images = this.querySelectorAll("img");
  images.forEach(function(image) {
    image.classList.toggle("d-none");
  });
}

productPhotos.forEach(function(product) {
  product.addEventListener("mouseover", toggleImage);
  product.addEventListener("mouseout", toggleImage);
});
