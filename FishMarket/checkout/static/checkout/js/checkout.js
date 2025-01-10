const slidesCount = document.querySelectorAll('.swiper0 .swiper-slide').length;
const slidesPerViewValue = slidesCount >= 2 ? 2 : 1;
let radioButtonChosen

if (slidesPerViewValue >= 2) {
    document.querySelector('.swiper0').style.height = '435px';
}

const swiper = new Swiper('.swiper0', {
    // Optional parameters
    direction: 'vertical',
    loop: false,
    watchOverflow: true,
    spaceBetween: 15,
    slidesPerView: slidesPerViewValue,
    mousewheel: {
        forceToAxis: true,
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

/*Показывает возможные варианты выбора города/отделения.
При выборе устанавливает input с выбранным городом так же обновляет скрытое поле input django forms
Очищает список для выбора.
*/
const swiper2 = new Swiper('.swiper1', {
    direction: 'vertical',
    loop: false,
    slidesPerView: 'auto',
    spaceBetween: 15,
    mousewheel: {
        forceToAxis: true,
    },
    scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
        snapOnRelease: true,
    },
    on: {
        click: function () {
            const clickedSlide = this.clickedSlide;
            if (clickedSlide) {
                let city_ref_input = document.querySelector('#cityRefHidden');

                if (!city_ref_input.value) {
                    const HiddenRef = clickedSlide.querySelector('.HiddenRef').textContent.trim()
                    const city_name = clickedSlide.querySelector('.option-text-title').textContent;
                    let search_input = document.querySelector('#site-search');
                    city_ref_input.value = HiddenRef;
                    search_input.value = city_name;
                    clear_swiper1();
                }
            }

        }
    }
});

function requestWarehouses(search_data) {
    let city_ref_input = document.querySelector('#cityRefHidden');

    if (city_ref_input && search_data) {
        $.ajax({
            url: novapost_warehouses,
            method: 'post',
            data: {
                'city_ref': city_ref_input,
                'csrfmiddlewaretoken': csrf,
                'typeofware': radioButtonChosen,
                'search_ware': search_data,
            },
            success: function (data) {
                let swiperItems = document.querySelector('.swiper-items');
                clear_swiper1();

                let htmlSwiperList = '';
                data.data_array.forEach(function (item) {
                    htmlSwiperList += `
                                <div class="swiper-slide">
                                    <div class="option-item">
                                        <div class="option-info-text">
                                            <p class="option-text-title">${radioButtonChosen['title']} -- №${item.number}</p>
                                            <p class="option-text-address">${item.address_ua}</p>
                                        </div>
                                    </div>
                                </div>`;
                })
                swiperItems.innerHTML = htmlSwiperList;
                swiper2.update();
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}


const element = document.getElementById('phonenumber');
const maskOptions = {
    mask: '+{38}(000)-000-00-00'
};
const mask = IMask(element, maskOptions);


document.addEventListener('change', function (event) {
    let deliveryType = document.querySelector('#typeOfDelivery');
    let city_ref_input = document.querySelector('#cityRefHidden');

    if (deliveryType && event.target.closest('#typeOfDelivery') && event.target.type === 'radio') {
        let novaposhtaButton = document.querySelector('#novaposhta-button');
        let novaposhtaButtonName = novaposhtaButton.querySelector('p');
        let novaposhtaWindowTitle = document.querySelector('.novaposhta-window-title-change');
        let novaposhtaInputWarehouse = document.querySelector('#warehouse-search');

        if (event.target) {
            radioButtonChosen = {
                'number': event.target.value,
                'title': event.target.closest('label').textContent.trim()
            };

            if (event.target.value === '1') {
                novaposhtaButtonName.innerText = 'Вибрати відділення'
                novaposhtaWindowTitle.innerText = 'Вибрати відділення'
                novaposhtaInputWarehouse.placeholder = 'Введіть номер відділення або адресу'
            } else if (event.target.value === '2') {
                novaposhtaButtonName.innerText = 'Вибрати Поштомат'
                novaposhtaWindowTitle.innerText = 'Вибрати Поштомат'
                novaposhtaInputWarehouse.placeholder = 'Введіть номер поштомату або адресу'
            } else if (event.target.value === '3') {
                novaposhtaButtonName.innerText = 'Кур\'єрська доставка'
                novaposhtaWindowTitle.innerText = 'Адреса доставки кур\'єром'
            }
        }

        novaposhtaButton.classList.remove('blured-div')
    }

    if (city_ref_input.value) {

    }
})

//Закрытия окна для выбора отделения, почтомата или курьера при клики в сторону
document.addEventListener('click', function (event) {
    let window = document.getElementsByClassName('novaposhta-window')[0];
    let background = document.querySelector('.novaposhta-container');

    if (background.contains(event.target) && !window.contains(event.target)) {
        background.style.display = 'none';
    }
})

//Получаем от пользователя input, и отсылаем его в request() or requestWarehouses()
document.addEventListener('DOMContentLoaded', function (event) {
    let time;
    let search_city = document.querySelector('#site-search');
    let search_warehouse = document.querySelector('#site-search');
    search_city.addEventListener('input', function () {
        clearTimeout(time);
        time = setTimeout(request, 800, search_city.value.trim())
    });

    search_warehouse.addEventListener('input', function () {
        clearTimeout(time);
        time = setTimeout(requestWarehouses, 800, search_warehouse.value.trim())
    });
})

// Делаем первую буквы заглавной
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function clear_swiper1() {
    let swiperItems = document.querySelector('.swiper-items');
    swiperItems.innerHTML = '';
    swiper2.update();
}

//Отсылаем запрос ajax на get_city и получаем array всех городов. После этого обновляем swiper2 список на странице.
function request(search_data) {
    if (search_data) {
        clear_swiper1()
        $.ajax({
            url: novapost_city,
            method: 'post',
            data: {
                'city': search_data,
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
                let swiperItems = document.querySelector('.swiper-items');
                let city_ref_input = document.querySelector('#cityRefHidden');
                city_ref_input.value = '';

                if (swiperItems) {
                    clear_swiper1()
                }
                let htmlSwiperList = '';
                data.data_array.forEach(function (item) {
                    htmlSwiperList += `
                                <div class="swiper-slide">
                                    <div class="option-item">
                                        <div class="option-info-text">
                                            <p class="option-text-title">${capitalizeFirstLetter(item.city_name_ua)}</p>
                                            <p class="option-text-address">${item.city_state}</p>
                                            <p class="HiddenRef">${item.ref_to_warehouses}</p>
                                        </div>
                                    </div>
                                </div>`;
                })
                swiperItems.innerHTML = htmlSwiperList;
                swiper2.update();
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}
