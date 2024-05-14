// contentScript.js

var currentUrl = window.location.href;
chrome.runtime.sendMessage({ action: 'sendUrl', url: currentUrl });
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    switch (message.action) {
        case 'displayPopup':
            displayPopup();
            break;
        case 'proceed':
            console.log("proceed to website");
            break;
        case 'cancel':
            console.log("quit website");
            break;
        default:
            break;
    }
});

function displayPopup() {
    const popupHtml = `
       <div id="popup-container" style="position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        color: black;
        padding: 20px;
        border: 2px solid black;
        z-index: 100;">
    <h1>This website is flagged as suspicious.</h1>
    <p>Do you want to proceed?</p>
    <button id="proceed-btn">Proceed</button>
    <button id="cancel-btn">Cancel</button>
</div>
    `;

    document.body.insertAdjacentHTML('afterbegin', popupHtml);

    const proceedBtn = document.getElementById('proceed-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    proceedBtn.addEventListener('click', function () {
        // Send a message to the background script indicating that the user wants to proceed
        chrome.runtime.sendMessage({ action: 'proceed' });
        closePopup(); // Close the popup
    });

    cancelBtn.addEventListener('click', function () {
        // Send a message to the background script indicating that the user wants to cancel
        chrome.runtime.sendMessage({ action: 'cancel' });
        closePopup(); // Close the popup
    });

    function closePopup() {
        document.getElementById('popup-container').remove();
    }
}
