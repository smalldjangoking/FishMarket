let dropdown = document.querySelector('.drop-down-category');
// Закрытие окна при клике вне его
document.addEventListener('click', function (e) {
    if (dropdown.style.display === 'flex' && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});