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
const swiper2 = new Swiper('.swiper2', {
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
                let search_city = document.querySelector('#city-search');
                let WareHouseIdForm = document.querySelector('#warehouseRefHidden');

                if (!city_ref_input.value) {
                    const HiddenRef = clickedSlide.querySelector('.HiddenRef').textContent.trim()
                    const city_name = clickedSlide.querySelector('.option-text-title').textContent;

                    city_ref_input.value = HiddenRef;
                    search_city.value = city_name;
                    clear_swiper2();
                    activate_warehouse();
                    return;
                }

                if (city_ref_input.value && search_city.value) {
                    WareHouseIdForm.value = clickedSlide.querySelector('.option-id-warehouse').textContent;
                    let WareHouseAddress = clickedSlide.querySelector('.option-text-address').textContent;
                    let novaware = document.querySelector('#warehouse-search');
                    novaware.value = clickedSlide.querySelector('.option-text-title').textContent;

                    novaposhtaButtonChange(WareHouseIdForm.value, WareHouseAddress)
                    NovaposhtaContainer()
                }
            }

        }
    }
});

function NovaposhtaContainer() {
    let novaposhtaContainer = document.querySelector('.novaposhta-container');
    novaposhtaContainer.style.display = 'none';
}


function novaposhtaButtonChange(warehouse_ref_hidden, warehouseAddress) {
    let city_ref_input = document.querySelector('#cityRefHidden');
    let buttonNovaPoshta = document.querySelector('#novaposhta-button');
    let buttonNovaPoshtaText = buttonNovaPoshta.querySelector('p');

    if (city_ref_input.value && warehouse_ref_hidden) {
        buttonNovaPoshtaText.innerText = capitalizeFirstLetter(warehouseAddress);
        let checkmark = document.querySelector('.button-img-container');
        checkmark.innerHTML = "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\" width=\"24px\" fill=\"#28a745\"><path d=\"m344-60-76-128-144-32 14-148-98-112 98-112-14-148 144-32 76-128 136 58 136-58 76 128 144 32-14 148 98 112-98 112 14 148-144 32-76 128-136-58-136 58Zm34-102 102-44 104 44 56-96 110-26-10-112 74-84-74-86 10-112-110-24-58-96-102 44-104-44-56 96-110 24 10 112-74 86 74 84-10 114 110 24 58 96Zm102-318Zm-42 142 226-226-56-58-170 170-86-84-56 56 142 142Z\"/></svg>";
    }
}

function activate_warehouse() {
    let novaware = document.querySelector('#warehouse-searchID');
    novaware.classList.remove('hidden-field');
    requestWarehouses();
}

function requestWarehouses(search_data) {
    let city_ref_input = document.querySelector('#cityRefHidden').value;
    if (city_ref_input && !radioButtonChosen['number'] === '3') {
        $.ajax({
            url: novapost_warehouses,
            method: 'post',
            data: {
                'city_ref': city_ref_input,
                'csrfmiddlewaretoken': csrf,
                'typeofware': radioButtonChosen['number'],
                'search_ware': search_data,
            },
            success: function (data) {
                let swiperItems = document.querySelector('.swiper-items');
                clear_swiper2();

                if (data.success) {
                    let htmlSwiperList = '';
                    data.data_array.forEach(function (item) {
                        htmlSwiperList += `
                                <div class="swiper-slide">
                                    <div class="option-item">
                                        <div class="option-info-text">
                                            <p class="option-text-title">${radioButtonChosen['title']} -- №${item.number}</p>
                                            <p class="option-text-address">${item.address_ua}</p>
                                            <p class="option-id-warehouse HiddenRef">${item.id}</p>
                                        </div>
                                    </div>
                                </div>`;
                    })
                    swiperItems.innerHTML = htmlSwiperList;
                    swiper2.update();
                } else if (!data.success) {
                    no_found_div()
                }
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

    if (deliveryType && event.target.closest('#typeOfDelivery') && event.target.type === 'radio') {
        let novaposhtaButton = document.querySelector('#novaposhta-button');
        let novaposhtaButtonName = novaposhtaButton.querySelector('p');
        let novaposhtaWindowTitle = document.querySelector('.novaposhta-window-title-change');
        let novaposhtaInputWarehouse = document.querySelector('#warehouse-search');
        let checkmark = document.querySelector('.button-img-container');
        let search_city = document.querySelector('#CitySearth-ware');
        let courier_delivery = document.querySelector('#novaposhta-input-courier');

        if (event.target) {
            radioButtonChosen = {
                'number': event.target.value,
                'title': event.target.closest('label').textContent.trim()
            };

            checkmark.innerHTML = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M5.49399 1.44891L10.0835 5.68541L10.1057 5.70593C10.4185 5.99458 10.6869 6.24237 10.8896 6.4638C11.1026 6.69642 11.293 6.95179 11.4023 7.27063C11.5643 7.74341 11.5643 8.25668 11.4023 8.72946C11.293 9.0483 11.1026 9.30367 10.8896 9.53629C10.6869 9.75771 10.4184 10.0055 10.1057 10.2942L10.0835 10.3147L5.49398 14.5511L4.47657 13.4489L9.06607 9.21246C9.40722 8.89756 9.62836 8.69258 9.78328 8.52338C9.93272 8.36015 9.96962 8.28306 9.98329 8.24318C10.0373 8.08559 10.0373 7.9145 9.98329 7.7569C9.96963 7.71702 9.93272 7.63993 9.78328 7.4767C9.62837 7.3075 9.40722 7.10252 9.06608 6.78761L4.47656 2.55112L5.49399 1.44891Z\" fill=\"#475569\"></path></svg>"
            novaposhtaButton.disabled = false;


            if (event.target.value === '1') {
                courier_delivery.classList.add('hidden-field');
                search_city.classList.remove('hidden-field');
                novaposhtaButtonName.innerText = 'Вибрати відділення'
                novaposhtaWindowTitle.innerText = 'Вибрати відділення'
                novaposhtaInputWarehouse.placeholder = 'Введіть номер відділення або адресу'
                reload_variables()
                PreparedSlidesForCity()
                swiper2.update();
            } else if (event.target.value === '2') {
                courier_delivery.classList.add('hidden-field');
                search_city.classList.remove('hidden-field');
                novaposhtaButtonName.innerText = 'Вибрати Поштомат'
                novaposhtaWindowTitle.innerText = 'Вибрати Поштомат'
                novaposhtaInputWarehouse.placeholder = 'Введіть номер поштомату або адресу'
                reload_variables()
            } else if (event.target.value === '3') {
                reload_variables()
                novaposhtaWindowTitle.innerText = 'Кур\'єрська доставка'
                search_city.classList.add('hidden-field');
                courier_delivery.classList.remove('hidden-field');

            }
        }
        novaposhtaButton.classList.remove('blured-div')
    }
})

function reload_variables() {
    let SwiperSlides = document.querySelector('.swiper-items')
    let search_city = document.querySelector('#city-search');
    let search_warehouse = document.querySelector('#warehouse-search');
    let city_ref_input = document.querySelector('#cityRefHidden');
    let WareHouseIdForm = document.querySelector('#warehouseRefHidden');
    let WareHouseIDDiv = document.querySelector('#warehouse-searchID');

    search_city.value = '';
    search_warehouse.value = '';
    SwiperSlides.innerHTML = '';
    swiper2.update();
    city_ref_input.value = '';
    WareHouseIdForm.value = '';
    WareHouseIDDiv.classList.add('hidden-field');
}

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
    let search_city = document.querySelector('#city-search');
    let search_warehouse = document.querySelector('#warehouse-search');

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

function clear_swiper2() {
    let swiperItems = document.querySelector('.swiper-items');
    swiperItems.innerHTML = '';
    swiper2.update();
}

function remove_warehouseSearch() {
    let warehouseSearchDiv = document.querySelector('#warehouse-searchID');
    let inputElement = warehouseSearchDiv.querySelector('input');
    if (inputElement) {
        inputElement.value = '';
    }
    warehouseSearchDiv.classList.add('hidden-field');
}


function no_found_div() {
    let swiperItems = document.querySelector('.swiper-items');
    swiperItems.innerHTML = '<div class="no-found-div"><p class="no-found-text">Пошук не дав результатів &#129300;</p></div>'
    swiper2.update();
}

//Отсылаем запрос ajax на get_city и получаем array всех городов. После этого обновляем swiper2 список на странице.
function request(search_data) {
    const warehouseInput = document.querySelector('#warehouse-searchID');
    if (!warehouseInput.classList.contains('hidden-field')) {
        remove_warehouseSearch()
    }

    if (search_data) {
        clear_swiper2()
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
                let WareHouseIdForm = document.querySelector('#warehouseRefHidden');
                city_ref_input.value = '';
                WareHouseIdForm.value = '';
                console.log(data)


                if (swiperItems) {
                    clear_swiper2()
                }

                if (data.success) {
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

                        swiperItems.innerHTML = htmlSwiperList;
                        swiper2.update();
                    })
                } else if (!data.success) {
                    no_found_div()
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function PreparedSlidesForCity() {
    const preparedSlidesList = `
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Харків</p>
                            <p class="option-text-address">(місто, Харківська обл.)</p>
                            <p class="HiddenRef">db5c88e0-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Київ</p>
                            <p class="option-text-address">(місто, Київська обл.)</p>
                            <p class="HiddenRef">8d5a980d-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Дніпро</p>
                            <p class="option-text-address">(місто, Дніпропетровська обл.)</p>
                            <p class="HiddenRef">db5c88f0-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Одеса</p>
                            <p class="option-text-address">(місто, Одеська обл.)</p>
                            <p class="HiddenRef">db5c88d0-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Львів</p>
                            <p class="option-text-address">(місто, Львівська обл.)</p>
                            <p class="HiddenRef">db5c88f5-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                <div class="swiper-slide">
                    <div class="option-item">
                        <div class="option-info-text">
                            <p class="option-text-title">Рівне</p>
                            <p class="option-text-address">(місто, Рівненська обл.)</p>
                            <p class="HiddenRef">db5c896a-391c-11dd-90d9-001a92567626</p>
                        </div>
                    </div>
                </div>
                `;
    let swiperItems = document.querySelector('.swiper-items');

    swiperItems.innerHTML = preparedSlidesList;
}
