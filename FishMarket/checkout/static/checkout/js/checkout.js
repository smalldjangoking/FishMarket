const slidesCount = document.querySelectorAll('.swiper .swiper-slide').length;
const slidesPerViewValue = slidesCount >= 2 ? 2 : 1;

if (slidesPerViewValue >= 2) {
    document.querySelector('.swiper').style.height = '435px';
}

const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'vertical',
    loop: false,
    watchOverflow: true,
    spaceBetween: 15,
    slidesPerView: slidesPerViewValue,
    mousewheel: {
        forceToAxis: true, // Скролл строго по вертикали
    },

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
        type: "fraction",
    },

    // And if we need scrollbar
    scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
        snapOnRelease: true,
    },
});


const element = document.getElementById('phonenumber');
const maskOptions = {
    mask: '+{38}(000)-000-00-00'
};

const mask = IMask(element, maskOptions);
