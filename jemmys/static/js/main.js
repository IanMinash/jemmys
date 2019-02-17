var productPhotos = document.querySelectorAll(".product .prod-photo");

function toggleSide() {
  var id = this.getAttribute("target");
  document.getElementById(id).classList.toggle("dismissed");
  document.getElementById("overlay").classList.toggle("show");
  setTimeout(() => {
    document.getElementById("overlay").classList.toggle("delay");
  }, 400);
}

document.querySelector("#show-nav").addEventListener("click", toggleSide);
document.querySelector("#dismiss-nav").addEventListener("click", toggleSide);
document.querySelector("#show-attr").addEventListener("click", toggleSide);
document.querySelector("#dismiss-attr").addEventListener("click", toggleSide);

function toggleImage() {
  images = this.querySelectorAll("img");
  if (images.length > 1) {
    images.forEach(function(image) {
      image.classList.toggle("d-none");
    });
  }
}

function oneToOne() {
  productPhotos.forEach(function(product) {
    if (Math.abs(product.offsetHeight - product.offsetWidth) > 2) {
      product.style.height = product.offsetWidth + "px";
    }
  });
}

var GETform = document.querySelector("#call_page");

function categoryRequest() {
  document.querySelector("#get_param").setAttribute("name", "category");
  document.querySelector("#get_param").setAttribute("value", this.innerHTML);
  GETform.submit();
}

productPhotos.forEach(function(product) {
  product.addEventListener("mouseover", toggleImage);
  product.addEventListener("mouseout", toggleImage);
});

window.addEventListener("load", oneToOne);
window.addEventListener("resize", oneToOne);

function asyncHttpGet(url, callback) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(xmlHttp.responseText);
  };
  xmlHttp.open("GET", url, true); // true for asynchronous
  xmlHttp.send(null);
}

function setSessionStorage(key, value) {
  sessionStorage.setItem(key, value);
}

function getLocation() {
  if (sessionStorage.getItem("city") == null) {
    asyncHttpGet("https://ipapi.co/json/", function(response) {
      var responseJSON = JSON.parse(response);
      setSessionStorage("city", responseJSON["city"]);
      $.post("{% url 'set-session' %}", {
        city: responseJSON["city"],
        csrfmiddlewaretoken: "{{ csrf_token }}"
      }).done(function(data) {
        if (data.statusText == "OK") {
          console.log("❤ Success");
        }
      });
    });
  }
}
