import numpy as np
import pickle
from urllib.parse import urlparse, quote
import ipaddress
import re
import requests
from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
import whois
import xgboost as xgb

# Function to check the presence of IP address in URL
def havingIP(url):
    try:
        ipaddress.ip_address(urlparse(url).netloc)
        return 1
    except ValueError:
        return 0

# Function to check the presence of "@" in URL
def haveAtSign(url):
    return 1 if "@" in url else 0

# Function to find the length of URL and categorize
def getLength(url):
    return 1 if len(url) >= 54 else 0

# Function to get the depth of URL
def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = sum(1 for i in s if i != '')
    return depth

# Function to check for redirection "//" in the URL
def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 and pos > 7 else 0

# Function to check existence of "HTTPS" token in the domain part of the URL
def httpDomain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

# Function to check use of URL Shortening Services
def tinyURL(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
    match = re.search(shortening_services, url)
    return 1 if match else 0

# Function to check for prefix or suffix separated by "-" in the domain
def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

# Function to check DNS record
def dnsRecord(domain):
    try:
        whois.whois(domain)
        return 0
    except Exception:
        return 1

# Function to calculate domain age
def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        return 0 if (ageofdomain / 30) > 6 else 1

# Function to check end time of domain
def domainEnd(domain_name):
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date, str):
        try:
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if expiration_date is None:
        return 1
    elif type(expiration_date) is list:
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        return 0 if (end / 30) > 6 else 1

# HTML and JavaScript based Features
# Function to check IFrame redirection
def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1

# Function to check mouse over event in status bar customization
def mouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0

# Function to check the status of the right-click attribute
def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1

# Function to check the number of forwardings
def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

# Function to extract all features from a URL
def featureExtraction(url):
    features = []
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))

    domain = urlparse(url).netloc
    try:
        domain_info = whois.whois(domain)
        dns = 0
    except:
        dns = 1
    features.append(dns)
    features.append(domainAge(domain_info) if dns == 0 else 1)
    features.append(domainEnd(domain_info) if dns == 0 else 1)

    try:
        response = requests.get(url)
    except:
        response = ""

    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))

    return features

# Load the pre-trained XGBoost model
with open('XGBoostClassifier.pickle.dat', 'rb') as model_file:
    model = pickle.load(model_file)

# Input URL
url_to_check = input("Enter the URL to check: ")

# Extract features from the URL
features = featureExtraction(url_to_check)
features_array = np.array(features).reshape(1, -1)  # Reshape for single sample prediction

# Predict the class probabilities
probabilities = model.predict_proba(features_array)
prob_phishing = probabilities[0][1]  # Assuming 1 is the index for phishing

# Output the prediction
if prob_phishing < 0.999:  # Adjust threshold as needed
    print("The URL is predicted to be Phishing.")
else:
    print("The URL is predicted to be Legitimate.")

print(f"Prediction Probabilities: {probabilities}")
print(f"Probabilities: {prob_phishing}")
print(f"Feature: {features}\n")
print(f"Feature: {features_array}")