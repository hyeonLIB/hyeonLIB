// /* When the user clicks on the button,
// toggle between hiding and showing the dropdown content */
// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
//     console.log("hello")
// }

// // Close the dropdown menu if the user clicks outside of it
// window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//             var dropdowns = document.getElementsByClassName("dropdown-content");
//             var i;
//             for (i = 0; i < dropdowns.length; i++) {
//                 var openDropdown = dropdowns[i];
//                 if (openDropdown.classList.contains('show')) {
//                     openDropdown.classList.remove('show');
//                 }
//             }
//     }
// }

// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
//   }
  
  // Close the dropdown if the user clicks outside of it

window.onclick = function(e) {
    if (!e.target.matches('.dropbtn')) {
    var myDropdown = document.getElementById("myDropdown");
      if (myDropdown.classList.contains('show')) {
        myDropdown.classList.remove('show');
      }
    }
  }

const btn_dropdown = document.querySelector(".dropbtn")
btn_dropdown.addEventListener('click', () => {
    const content_dropdown = document.getElementById("myDropdown")
    content_dropdown.classList.toggle("show")
    return content_dropdown
})