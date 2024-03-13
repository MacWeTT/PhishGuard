let API_URL = "http://localhost:8000/";

setTimeout(() => {
    fetch(API_URL)
        .then(res => res.json())
        .then((data) => {
            const para = document.getElementById("para");
            para.innerHTML = data.message;
        })
        .catch(err => console.error(err))
}, 2000);

