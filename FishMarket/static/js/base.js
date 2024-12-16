let dropdown = document.querySelector('.drop-down-category');
// Закрытие окна при клике вне его
document.addEventListener('click', function (e) {
    if (dropdown.style.display === 'flex' && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});

// уменьшение nav для mobile
document.addEventListener("scroll", function () {
    var scroll = window.scrollY;
    var nav = document.querySelector("nav");
    var header = document.querySelector("header");


    if (scroll > 100) {
        nav.querySelector("a").style.display = "none";
        nav.classList.add("active");
        header.classList.add("active");

    } else {
        nav.querySelector("a").style.display = "flex";
        nav.classList.remove("active");
        header.classList.remove("active");
    }
});