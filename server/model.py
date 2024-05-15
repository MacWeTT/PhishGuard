from urllib.parse import urlparse
import numpy as np
import pickle
import math
import re


# Function to count the number of dots in a string
def count_dots(string):
    return string.count(".")


# Function to count the number of repeated digits in a string
def count_repeated_digits(string):
    return len([c for c in string if c.isdigit() and string.count(c) > 1])


# Function to count the number of special characters in a string
def count_special_chars(string, exclude=""):
    special_chars = r"[^a-zA-Z0-9]"
    if exclude:
        special_chars = r"[" + re.escape(exclude) + r"]"
    return len(re.findall(special_chars, string))


# Function to count the number of subdomains
def count_subdomains(domain):
    return len(domain.split(".")) - 2


# Function to calculate the entropy of a string
def calculate_entropy(string):
    entropy = 0
    for char in set(string):
        p = string.count(char) / len(string)
        entropy += -p * math.log2(p)
    return entropy


# Function to extract features from a URL
def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    url_length = len(url)
    number_of_dots_in_url = count_dots(url)
    having_repeated_digits_in_url = int(count_repeated_digits(url) > 0)
    number_of_digits_in_url = sum(c.isdigit() for c in url)
    number_of_special_char_in_url = count_special_chars(url)
    number_of_hyphens_in_url = url.count("-")
    number_of_underline_in_url = url.count("_")
    number_of_slash_in_url = url.count("/")
    number_of_questionmark_in_url = url.count("?")
    number_of_equal_in_url = url.count("=")
    number_of_at_in_url = url.count("@")
    number_of_dollar_in_url = url.count("$")
    number_of_exclamation_in_url = url.count("!")
    number_of_hashtag_in_url = url.count("#")
    number_of_percent_in_url = url.count("%")

    domain_length = len(domain)
    number_of_dots_in_domain = count_dots(domain)
    number_of_hyphens_in_domain = domain.count("-")
    having_special_characters_in_domain = int(count_special_chars(domain) > 0)
    number_of_special_characters_in_domain = count_special_chars(domain)
    having_digits_in_domain = int(any(c.isdigit() for c in domain))
    number_of_digits_in_domain = sum(c.isdigit() for c in domain)
    having_repeated_digits_in_domain = int(count_repeated_digits(domain) > 0)

    number_of_subdomains = count_subdomains(domain)
    having_dot_in_subdomain = int(any("." in sub for sub in domain.split(".")[:-2]))
    having_hyphen_in_subdomain = int(any("-" in sub for sub in domain.split(".")[:-2]))
    average_subdomain_length = (
        sum(len(sub) for sub in domain.split(".")[:-2]) / number_of_subdomains
        if number_of_subdomains
        else 0
    )
    average_number_of_dots_in_subdomain = (
        sum(count_dots(sub) for sub in domain.split(".")[:-2]) / number_of_subdomains
        if number_of_subdomains
        else 0
    )
    average_number_of_hyphens_in_subdomain = (
        sum(sub.count("-") for sub in domain.split(".")[:-2]) / number_of_subdomains
        if number_of_subdomains
        else 0
    )
    having_special_characters_in_subdomain = int(
        any(count_special_chars(sub) for sub in domain.split(".")[:-2])
    )
    number_of_special_characters_in_subdomain = sum(
        count_special_chars(sub) for sub in domain.split(".")[:-2]
    )
    having_digits_in_subdomain = int(
        any(any(c.isdigit() for c in sub) for sub in domain.split(".")[:-2])
    )
    number_of_digits_in_subdomain = sum(
        sum(c.isdigit() for c in sub) for sub in domain.split(".")[:-2]
    )
    having_repeated_digits_in_subdomain = int(
        any(count_repeated_digits(sub) for sub in domain.split(".")[:-2])
    )

    having_path = int(bool(parsed_url.path))
    path_length = len(parsed_url.path)
    having_query = int(bool(parsed_url.query))
    having_fragment = int(bool(parsed_url.fragment))
    having_anchor = int(bool(parsed_url.fragment and "#" in parsed_url.fragment))

    entropy_of_url = calculate_entropy(url)
    entropy_of_domain = calculate_entropy(domain)

    features = [
        url_length,
        number_of_dots_in_url,
        having_repeated_digits_in_url,
        number_of_digits_in_url,
        number_of_special_char_in_url,
        number_of_hyphens_in_url,
        number_of_underline_in_url,
        number_of_slash_in_url,
        number_of_questionmark_in_url,
        number_of_equal_in_url,
        number_of_at_in_url,
        number_of_dollar_in_url,
        number_of_exclamation_in_url,
        number_of_hashtag_in_url,
        number_of_percent_in_url,
        domain_length,
        number_of_dots_in_domain,
        number_of_hyphens_in_domain,
        having_special_characters_in_domain,
        number_of_special_characters_in_domain,
        having_digits_in_domain,
        number_of_digits_in_domain,
        having_repeated_digits_in_domain,
        number_of_subdomains,
        having_dot_in_subdomain,
        having_hyphen_in_subdomain,
        average_subdomain_length,
        average_number_of_dots_in_subdomain,
        average_number_of_hyphens_in_subdomain,
        having_special_characters_in_subdomain,
        number_of_special_characters_in_subdomain,
        having_digits_in_subdomain,
        number_of_digits_in_subdomain,
        having_repeated_digits_in_subdomain,
        having_path,
        path_length,
        having_query,
        having_fragment,
        having_anchor,
        entropy_of_url,
        entropy_of_domain,
    ]

    return features


def checkForPhishing(url: str) -> dict:
    with open("./model/XGBoostClassifier.pickle.dat", "rb") as model_file:
        model = pickle.load(model_file)
        features = extract_features(url)
        features_array = np.array(features).reshape(1, -1)
        probabilities = model.predict_proba(features_array)

        phishing = round(probabilities[0][1] * 100, 2)
        legitimate = round(probabilities[0][0] * 100, 2)

        if phishing > legitimate:
            verdict = "Website is predicted to be phishy. Please proceed with caution."
            code = 1
        else:
            verdict = "Website is predicted to be safe. Safe surfing!"
            code = 0

    return {
        "code": code,
        "verdict": verdict,
        "Phishing": f"{phishing}",
        "Legitimate": f"{legitimate}",
    }
