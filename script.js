var menuIcon = document.querySelector('.menu-icon');
var sidebar = document.querySelector('.sidebar');
var container = document.querySelector('.container');


// menuIcon.onclick = function(){
//     sidebar.classList.toggle('hide-sidebar');
//     container.classList.toggle('container-widen');
// }

menuIcon.addEventListener('click', ()=> {
    sidebar.classList.toggle('hide-sidebar');
    container.classList.toggle('container-widen');
})
