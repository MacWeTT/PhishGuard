document.addEventListener("DOMContentLoaded", function () {
    // function updateDetailsFromLocalStorage() {
    //     const storedData = localStorage.getItem('website-details');
    //     if (storedData) {
    //         const data = JSON.parse(storedData);
    //         document.getElementById('phishing-rate').innerText = data.phishing;
    //         document.getElementById('legitimate-rate').innerText = data.legitimate;
    //         document.getElementById('verdict-message').innerText = data.verdict;
    //     }
    // }


    // updateDetailsFromLocalStorage();
    // console.log(data)
    // setInterval(updateDetailsFromLocalStorage, 5000);

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
