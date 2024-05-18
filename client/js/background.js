// background.js
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    switch (message.action) {
        case 'sendUrl':
            sendUrlToBackend(message.url);
            break;
        case 'closeTab':
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                let tabId = tabs[0].id;
                chrome.tabs.remove(tabId);
            });
        default:
            break;
    }
});

function sendUrlToBackend(url) {
    const API_URL = `http://localhost:8000/check-url?url=${encodeURIComponent(url)}`;
    fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.code === 1) {
                // Send message to content script to display popup
                chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: 'displayPopup', data: data });

                });
            } else {
                console.log('No action required.');
            }
        })
        .catch(error => {
            console.error('Error sending URL to backend:', error);
        });
}
