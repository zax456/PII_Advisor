// When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction(navbar, sticky)};

var navbar, sticky = window.onload = function() {
  setTimeout(
    function() {
      // Get the navbar
      navbar = document.getElementById("navbar")

      // Get the offset position of the navbar
      sticky = navbar.offsetTop;
      return navbar, sticky
    }, 2000);
};


// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction(navbar, sticky) {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } 
  else {
    navbar.classList.remove("sticky")
  }
}