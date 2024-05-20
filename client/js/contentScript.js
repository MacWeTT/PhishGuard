var currentUrl = window.location.href;

chrome.runtime.sendMessage({ action: 'sendUrl', url: currentUrl });

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    switch (message.action) {
        case 'displayPopup':
            createPopup(message.data);
            updateExtension(message.data)
            break;
        default:
            break;
    }
});

const popupStyles =
    `
:root {
  --primary-color: #496989;
  --secondary-color: #58a399;
  --tertiary-color: #a8cd9f;
  --quaternary-color: #e2f4c5;
  --success-color: #4bb543;
  --danger-color: #7a0012;
  --warning-color: #eed202;
}

.popup-parent {
  position: fixed; /* Change from absolute to fixed to ensure the popup stays centered when scrolling */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(4px);
  z-index: 99999;
}

.warning {
  border: 5px solid var(--warning-color);
}

.danger {
  border: 5px solid var(--danger-color);
}

.popup-container {
  background-color: var(--quaternary-color);
  color: black;
  padding: 20px;
  border-radius: 10px;
  z-index: 99999;
  /* Remove transform translate, it's not necessary for centering */
}

.probabilities {
  display: flex;
  justify-content: space-evenly;
  margin-top: 10px;
  font-size: 20px;
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

.popup {
  overflow: hidden;
}
`

function createPopup(data) {
    const popupParent = document.createElement('div');
    popupParent.classList.add('popup-parent');

    const popupContainer = document.createElement('div');
    popupContainer.classList.add('popup-container');
    if (data.code === 1) {
        popupContainer.classList.add('warning')
    } else if (data.code === 2) {
        popupContainer.classList.add('danger')
    }

    const heading = document.createElement('h1');
    heading.style.color = 'var(--primary-color)';
    heading.textContent = data.verdict;

    const probabilities = document.createElement('div');
    probabilities.classList.add('probabilities');

    const legitimate = document.createElement('div');
    legitimate.classList.add('probability-item');
    legitimate.textContent = `Legitimate: ${data.legitimate}%`;

    const phishing = document.createElement('div');
    phishing.classList.add('probability-item');
    phishing.textContent = `Phishing: ${data.phishing}%`;

    probabilities.appendChild(legitimate);
    probabilities.appendChild(phishing);

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
    popupContainer.appendChild(probabilities);
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

document.addEventListener('DOMContentLoaded', function (data) {
    console.log(data);
    const verdictRing = document.getElementById('verdict');
    const verdictRate = document.getElementById('verdict-rate');
    const verdictMessage = document.getElementById('verdict-message');
    console.log(verdictRing)

    verdictRate.textContent = `${data.phishing.toFixed(2)}%`;
    document.getElementById('phishing-rate').textContent = `${data.phishing.toFixed(2)}%`;
    document.getElementById('legitimate-rate').textContent = `${data.legitimate.toFixed(2)}%`;
    verdictMessage.textContent = data.verdict;

    if (data.code === 1) {
        verdictRing.style.backgroundColor = 'var(--danger-color)';
    } else {
        verdictRing.style.backgroundColor = 'var(--success-color)';
    }
})
