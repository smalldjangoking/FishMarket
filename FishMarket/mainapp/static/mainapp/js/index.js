const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    loop: true, // Цикличный слайдер
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    spaceBetween: 15,
});

document.addEventListener("scroll", function () {
    var scroll = window.scrollY;
    var nav = document.querySelector("nav");

    if (scroll > 100) {
        nav.style.background = "linear-gradient(#1e3a8a, #3b82f6)";
    } else {
        nav.style.background = "";
    }
});