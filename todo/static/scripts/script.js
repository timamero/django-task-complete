const navBurger = document.querySelector('.navbar-burger');
const menuItems = document.querySelector('.navbar-menu');

navBurger.addEventListener('click', function(e) {
    navBurger.classList.toggle('is-active');
    menuItems.classList.toggle('is-active');
})