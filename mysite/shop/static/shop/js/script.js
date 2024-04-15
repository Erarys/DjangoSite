function change_display(window, style) {
    window.style.display = style
}

document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll('.leave_call');
    var popup_window = document.querySelector('.popup-window');
    var send_button = document.querySelector('.send_button');
    var block = document.querySelector('.popup-window')
    var buttons_product = document.querySelectorAll('.product');

    buttons_product.forEach(function (button) {
        button.addEventListener('click', function () {
            var link = "http://127.0.0.1:8000/products";

            // Проверяем, есть ли ссылка
            if (link) {
                // Переходим по ссылке
                window.location.href = link;
            }
        });
    });


    for (let i = 0; i < buttons.length; i++) {
        buttons[i].addEventListener('click', function () {
            change_display(popup_window, 'flex')

        });
    }

    send_button.addEventListener('click', function () {
        change_display(popup_window, 'none')
    });

    block.addEventListener('click', function (event) {
        if (event.target === block) {
            change_display(popup_window, 'none')
        }

    });


});