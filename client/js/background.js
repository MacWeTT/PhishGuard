// background.js

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'sendUrl') {
        sendUrlToBackend(message.url);
    }
});

function sendUrlToBackend(url) {
    const API_URL = "http://localhost:8000/check-url/";

    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Result from backend:', data);
            if (data.code === 1) { // Check if code is equal to 1
                // Send a message to the content script to display the popup
                chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: 'displayPopup' });
                });
            } else {
                // Store the result if legitimate or handle other cases
                console.log('Backend response is not suspicious:', data);
            }
        })
        .catch(error => {
            console.error('Error sending URL to backend:', error);
        });
}
