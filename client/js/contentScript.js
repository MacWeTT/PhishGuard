// contentScript.js

// Extract the current URL of the webpage
var currentUrl = window.location.href;

// Send the URL to the background script
chrome.runtime.sendMessage({ url: currentUrl });
