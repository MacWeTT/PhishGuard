document.addEventListener("DOMContentLoaded", function () {
    const API_URL = "http://localhost:8000/";
    const online_button = document.querySelector('.online-status');
    const extension_status = document.querySelector('.extension-status');
    console.log(online_button, extension_status)
    fetch(API_URL)
        .then(res => res.json())
        .then((data) => {
            online_button.style.backgroundColor = 'green';
            extension_status.innerHTML = data.message;
        })
        .catch((err) => {
            extension_status.innerHTML = 'Cannot connect to server.';
        });
});
