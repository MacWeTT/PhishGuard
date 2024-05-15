var currentUrl = window.location.href;

chrome.runtime.sendMessage({ action: 'sendUrl', url: currentUrl });

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    switch (message.action) {
        case 'displayPopup':
            createPopup();
            break;
        default:
            break;
    }
});

const popupStyles =
    `:root {
        --primary-color: #496989;
        --secondary-color: #58a399;
        --tertiary-color: #a8cd9f;
        --quaternary-color: #e2f4c5;
    }

    .popup-parent {
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background-size: cover;
        background-position: center;
        height: 100vh;
        overflow: hidden;
        z-index: 99999;
    }

    .popup-parent {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(4px);
    }

    .popup-container {
        background-color: var(--quaternary-color);
        color: black;
        padding: 20px;
        border: 2px solid var(--secondary-color);
        border-radius: 10px;
    }

    .popup-text {
        font-size: 20px;
        text-align: center;
    }

    .popup-buttons {
        display: flex;
        justify-content: space-evenly;
        align-items: center;
    }


    #proceed-btn,
    #cancel-btn {
        padding: 5px 10px;
        margin: 10px;
        border: 2px solid var(--secondary-color);
        color: var(--primary-color);
        background-color: var(--quaternary-color);
        cursor: pointer;
        border-radius: 4px;
    }

    .popup{
        overflow: hidden;
    }
`;

function createPopup() {
    const popupParent = document.createElement('div');
    popupParent.classList.add('popup-parent');

    const popupContainer = document.createElement('div');
    popupContainer.classList.add('popup-container');

    const heading = document.createElement('h1');
    heading.style.color = 'var(--primary-color)';
    heading.textContent = 'This website is flagged as suspicious.';

    const paragraph = document.createElement('p');
    paragraph.classList.add('popup-text');
    paragraph.textContent = 'Do you want to proceed?';

    const buttonsDiv = document.createElement('div');
    buttonsDiv.classList.add('popup-buttons');

    const proceedBtn = document.createElement('button');
    proceedBtn.id = 'proceed-btn';
    proceedBtn.textContent = 'I know what I\'m doing';

    const cancelBtn = document.createElement('button');
    cancelBtn.id = 'cancel-btn';
    cancelBtn.textContent = 'Take me to safety';

    // Append elements
    buttonsDiv.appendChild(proceedBtn);
    buttonsDiv.appendChild(cancelBtn);
    popupContainer.appendChild(heading);
    popupContainer.appendChild(paragraph);
    popupContainer.appendChild(buttonsDiv);
    popupParent.appendChild(popupContainer);

    // Append the popup to the body
    document.body.appendChild(popupParent);

    const styleElement = document.createElement('style');
    styleElement.textContent = popupStyles;
    document.head.appendChild(styleElement);
    document.body.classList.toggle('popup');

    // Event listeners for buttons
    proceedBtn.addEventListener('click', function () {
        popupParent.remove();
        document.body.classList.toggle('popup');
    });

    cancelBtn.addEventListener('click', function () {
        chrome.runtime.sendMessage({ action: 'closeTab' });
    });
}
