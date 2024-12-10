document.addEventListener('DOMContentLoaded', function
    () {
    const minPriceInput = document.getElementById('minPriceInput');
    const maxPriceInput = document.getElementById('maxPriceInput');
    const slider = document.getElementById('price-slider');

    noUiSlider.create(slider, {
        start: [parseInt(minPriceInput.value), parseInt(maxPriceInput.value)],
        connect: true,
        range: {
            'min': parseInt(minPriceInput.min),
            'max': parseInt(maxPriceInput.max),
        },
        step: 1,
        format: {
            to: value => Math.round(value),
            from: value => Number(value)
        }
    });

    slider.noUiSlider.on('update', function (values, handle) {
        if (handle === 0) {
            minPriceInput.value = values[0];
        } else {
            maxPriceInput.value = values[1];
        }
    });

    minPriceInput.addEventListener('change', function () {
        const minPrice = Math.min(parseInt(minPriceInput.value), parseInt(maxPriceInput.value, 10));
        slider.noUiSlider.set([minPrice, null]);
        updateProducts();
    });

    maxPriceInput.addEventListener('change', function () {
        const maxPrice = Math.max(parseInt(maxPriceInput.value), parseInt(minPriceInput.value));
        slider.noUiSlider.set([null, maxPrice]);
        updateProducts();
    });

    slider.noUiSlider.on('change', updateProducts);

    function updateProducts() {
        const minPrice = minPriceInput.value;
        const maxPrice = maxPriceInput.value;
        const params = new URLSearchParams(window.location.search);
        params.set('min_price', minPrice);
        params.set('max_price', maxPrice);
        window.location.search = params.toString();
    }
});

document.addEventListener('click', function (e) {
    const product_dropdown = document.querySelector('.price-filter-dropmenu');
    const product_dropdown_main = document.querySelector('.product-dropmenu-container');
    let product_drop_menu_desk = document.querySelector('.product-dropmenu-desk');
    const close_filter_btn = document.querySelector('.close-filter-btn');

    if (product_dropdown_main.contains(e.target)) {
        product_drop_menu_desk.style.background = '#1e90ff';
        product_drop_menu_desk.style.color = 'white';
    }

    if (
        (product_dropdown.classList.contains('active') &&
        !product_dropdown.contains(e.target) &&
        !product_dropdown_main.contains(e.target)) || close_filter_btn.contains(e.target)
    ) {
        product_dropdown.classList.remove('active');
        product_drop_menu_desk.style.background = 'white';
        product_drop_menu_desk.style.color = '#B721FF';
    }
});



