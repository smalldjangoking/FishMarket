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


document.addEventListener('change', function (event) {
    let deliveryType = document.querySelector('#typeOfDelivery');
    if (deliveryType && event.target.closest('#typeOfDelivery') && event.target.type === 'radio') {
        let novaposhtaButton = document.querySelector('#novaposhta-button');
        let novaposhtaButtonName = novaposhtaButton.querySelector('p');
        let novaposhtaWindowTitle = document.querySelector('.novaposhta-window-title-change');
        if (event.target.value === '1') {
            novaposhtaButtonName.innerText = 'Вибрати відділення'
            novaposhtaWindowTitle.innerText = 'Вибрати відділення'
        } else if (event.target.value === '2') {
            novaposhtaButtonName.innerText = 'Вибрати Поштомат'
            novaposhtaWindowTitle.innerText = 'Вибрати Поштомат'
        } else if (event.target.value === '3') {
            novaposhtaButtonName.innerText = 'Кур\'єрська доставка'
            novaposhtaWindowTitle.innerText = 'Адреса доставки кур\'єром'
        }

        novaposhtaButton.classList.remove('blured-div')
    }
})

document.addEventListener('click', function (event) {
    let window = document.getElementsByClassName('novaposhta-window')[0];
    let background = document.querySelector('.novaposhta-container');

    if (background.contains(event.target) && !window.contains(event.target)) {
        background.style.display = 'none';
    }
})

document.addEventListener('DOMContentLoaded', function (event) {
    let time;
    let search_input = document.querySelector('#site-search');
    search_input.addEventListener('input', function () {
        clearTimeout(time);
        time = setTimeout(request, 800, search_input.value.trim())
    });
})

function request(search_data) {
    if (search_data) {
        console.log(search_data);
    }
}
