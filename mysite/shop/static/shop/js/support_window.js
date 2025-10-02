document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("chat-header");
    const body = document.getElementById("chat-body");

    if (!header.dataset.listenerAttached) {
        header.dataset.listenerAttached = "true";

        header.addEventListener("click", function () {
            const currentDisplay = window.getComputedStyle(body).display;

            body.style.display = (currentDisplay === "none") ? "block" : "none";
        });
    }

});
