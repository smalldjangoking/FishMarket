const slidesCount = document.querySelectorAll('.swiper0 .swiper-slide').length;
const slidesPerViewValue = slidesCount >= 2 ? 2 : 1;
const ArrowSvg = "<svg width=\"16\" height=\"16\" viewBox=\"0 0 16 16\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M5.49399 1.44891L10.0835 5.68541L10.1057 5.70593C10.4185 5.99458 10.6869 6.24237 10.8896 6.4638C11.1026 6.69642 11.293 6.95179 11.4023 7.27063C11.5643 7.74341 11.5643 8.25668 11.4023 8.72946C11.293 9.0483 11.1026 9.30367 10.8896 9.53629C10.6869 9.75771 10.4184 10.0055 10.1057 10.2942L10.0835 10.3147L5.49398 14.5511L4.47657 13.4489L9.06607 9.21246C9.40722 8.89756 9.62836 8.69258 9.78328 8.52338C9.93272 8.36015 9.96962 8.28306 9.98329 8.24318C10.0373 8.08559 10.0373 7.9145 9.98329 7.7569C9.96963 7.71702 9.93272 7.63993 9.78328 7.4767C9.62837 7.3075 9.40722 7.10252 9.06608 6.78761L4.47656 2.55112L5.49399 1.44891Z\" fill=\"#475569\"></path></svg>"
const CheckMarkGreen = "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\" width=\"24px\" fill=\"#28a745\"><path d=\"m344-60-76-128-144-32 14-148-98-112 98-112-14-148 144-32 76-128 136 58 136-58 76 128 144 32-14 148 98 112-98 112 14 148-144 32-76 128-136-58-136 58Zm34-102 102-44 104 44 56-96 110-26-10-112 74-84-74-86 10-112-110-24-58-96-102 44-104-44-56 96-110 24 10 112-74 86 74 84-10 114 110 24 58 96Zm102-318Zm-42 142 226-226-56-58-170 170-86-84-56 56 142 142Z\"/></svg>";
if (slidesPerViewValue >= 2) {
    document.querySelector('.swiper0').style.height = '435px';
}
let NovaPoshtaButton = document.querySelector('#novaposhta-button')
let UserDeliveryAddress
let UserSavedAddressId
let UserAddressesContainer
let UsersAddressesButton
let CityChosen = false;
let WarehouseChosen = false;
const element = document.getElementById('phonenumber');
const maskOptions = {
    mask: '+{38}(000)-000-00-00'
};
const mask = IMask(element, maskOptions);
let search_city = document.querySelector('#city-search');
let search_warehouse = document.querySelector('#warehouse-search');
const courier_form = document.querySelector('#novaposhta-input-courier');
let CourierHiddenFormField = document.querySelector('#courierHidden');


//Slider for View Cart
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

//Slider for selection from User addresses
const swiper3 = new Swiper('.swiper3', {
    // Optional parameters
    direction: 'vertical',
    loop: false,
    watchOverflow: true,
    spaceBetween: 15,
    slidesPerView: slidesPerViewValue,
    mousewheel: {
        forceToAxis: true,
    },

    on: {
        click: function () {
            const clickedSlide = this.clickedSlide;
            if (clickedSlide) {
                UserDeliveryAddress = clickedSlide.innerText;
                UserSavedAddressId = clickedSlide.querySelector('.address-id').textContent.trim();

                CloseUserSavedAddresses(UserDeliveryAddress)

            }
        }
    },
    scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
        snapOnRelease: true,
    },
});

//Close Window's delivery option
document.addEventListener('click', function (event) {
    UserAddressesContainer = document.querySelector('.novaposhta-users-addresses');
    let NovaposhtaContainer = document.querySelector('.novaposhta-container');
    //Closing user's saved delivery list
    if (event.target.classList.contains('novaposhta-users-addresses') && !event.target.classList.contains('novaposhta-window')) {
        UserAddressesContainer.style.display = 'none';
    }
    //Closing novaposhta container
    if (event.target.classList.contains('novaposhta-container') && !event.target.classList.contains('novaposhta-window')) {
        NovaposhtaContainer.style.display = 'none';
    }
})

//Choose for City,Warehouse and parcel terminal
const swiper2 = new Swiper('.swiper2', {
    direction: 'vertical',
    loop: false,
    slidesPerView: 'auto',
    spaceBetween: 15,
    mousewheel: {
        forceToAxis: true,
    },

    on: {
        click: function () {
            const clickedSlide = this.clickedSlide;

        }
    },
    scrollbar: {
        el: '.swiper-scrollbar',
        draggable: true,
        snapOnRelease: true,
    },
})

//If typeOfDelivery is chosen, opens diffrent variations of search in novaposhta container
document.getElementById('typeOfDelivery').addEventListener('change', function (event) {
    let title = document.querySelector('.novaposhta-window-title-change');
    let NovaPoshtaButtonTitle = NovaPoshtaButton.querySelector('.text-grey');

    if (event.target.value === '1') {
        NovaPoshtaButtonTitle.innerText = 'Вибрати відділення';
        title.innerText = 'Вибрати відділення';
        //novaposhtaInputWarehouse.placeholder = 'Введіть номер відділення або адресу';
    } else if (event.target.value === '2') {
        NovaPoshtaButtonTitle.innerText = 'Вибрати Поштомат';
        title.innerText = 'Вибрати Поштомат';
        //novaposhtaInputWarehouse.placeholder = 'Введіть номер поштомату або адресу';
    } else if (event.target.value === '3') {
        title.innerText = 'Кур\'єрська доставка';
        NovaPoshtaButtonTitle.innerText = 'Кур\'єрська доставка';
    }
    //activator for button novaposhta
    NovaPoshtaButton.classList.remove('blured-div');
    NovaPoshtaButton.disabled = false;
})

function CloseUserSavedAddresses(UserDeliveryAddress) {
    UserAddressesContainer.style.display = 'none';
    UsersAddressesButton = document.querySelector('#UsersAddressesButton');
    UsersAddressesButton.querySelector('p').innerText = UserDeliveryAddress
    UsersAddressesButton.querySelector('.button-img-container').innerHTML = CheckMarkGreen

}

//Listening Inputs for value (City,warehouse, parcel-terminal, courier fields check)
document.addEventListener('DOMContentLoaded', function (event) {
    let time;
    const inputs = courier_form.querySelectorAll('input');

    //Listening City Search
    search_city.addEventListener('input', function () {
        clearTimeout(time);
        time = setTimeout(city_request, 800, search_city.value.trim())
    });

    //Listening Warehouse Search
    search_warehouse.addEventListener('input', function () {
        clearTimeout(time);
        time = setTimeout(requestWarehouses, 800, search_warehouse.value.trim())
    });

    //Listening Courier Fields
    courier_form.addEventListener('input', function () {
        let allInputs = true

        inputs.forEach(input => {
            if (input.id === 'courier-field-apartment') {
                return;
            }

            if (!input.value.trim()) {
                allInputs = false;
            }
        });

        if (allInputs) {
            AwakeButtonCourier(true);
        } else if (!allInputs) {
            AwakeButtonCourier(false);
        }
    });
})

function AwakeButtonCourier(awake) {
    let AwakeButtonCourier = document.querySelector('#AwakeButtonCourier');
    if (awake) {
        AwakeButtonCourier.classList.remove('blured-div');
        AwakeButtonCourier.disabled = false;
    } else if (!awake) {
        AwakeButtonCourier.classList.add('blured-div');
        AwakeButtonCourier.disabled = true;
    }
}


function courierButtonSubmit() {
    const city = document.querySelector('#courier-field-city').value;
    const street = document.querySelector('#courier-field-street').value;
    const house = document.querySelector('#courier-field-house').value;
    const apartment = document.querySelector('#courier-field-apartment').value;

    if (city && street && house) {
        const data = {
            city: city,
            street: street,
            house: house,
            apartment: apartment,
        };

        CourierHiddenFormField.value = JSON.stringify(data);
        novaposhtaButtonChangeCourier(city, street, house, apartment);
    }
}

//Sending city input to backEnd.
function city_request(search_data) {
    if (search_data) {
        $.ajax({
            url: novapost_city,
            method: 'post',
            data: {
                'city': search_data,
                'csrfmiddlewaretoken': csrf,
            },
            success: function (data) {
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
                    no_found_div();
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function iterator_array(iterable) {
    iterable.forEach(function (item) {
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
    }
}