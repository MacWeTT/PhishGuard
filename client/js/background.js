// background.js

// Listen for messages from content script
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    console.log('Message received:', message);
    sendUrlToBackend(message.url);
    console.log("Request sent");
});

// Function to send URL to backend server
function sendUrlToBackend(url) {
    // Use AJAX or Fetch API to send the URL to your backend server
    // Example using Fetch API
    fetch(`http://localhost:8000/check-url`, {
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
            console.log('Response from backend:', data);
        })
        .catch(error => {
            console.error('Error sending URL to backend:', error);
        });
}
