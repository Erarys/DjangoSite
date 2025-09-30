document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById("chat-header");
    const body = document.getElementById("chat-body");

    // проверяем, есть ли уже флаг
    if (!header.dataset.listenerAttached) {
        header.dataset.listenerAttached = "true";

        header.addEventListener("click", function () {
            body.style.display = body.style.display === "none" ? "block" : "none";
        });
    }
});
