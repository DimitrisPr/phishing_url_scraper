from difflib import SequenceMatcher
from io import StringIO
import requests
import zlib
import json
import re


def download_phishing_data():

    PHISHTANK_API_KEY = 'insert_api_key_here'

    print("\n Downloading feeds")
    print(" This may take some minutes...\n")

    # Array containing the links of the phishing feed sources
    feed_sources = [
        "https://openphish.com/feed.txt",
        "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt",
        "http://data.phishtank.com/data/" + PHISHTANK_API_KEY + "/online-valid.json.gz"]

    # Save phishing urls in a list
    phishing_URLs = []
    for feed in feed_sources:

        print(" Downloading: " + feed + "\n")

        response = requests.get(feed)
        if 'json.gz' in feed:
            decompressed_data = zlib.decompress(response.content, 16 + zlib.MAX_WBITS)
            json_file = json.loads(decompressed_data.decode('utf-8'))

            for json_object in json_file:

                url = json_object['url']
                phishing_URLs.append(url)
        else:
            url = response.text.split("\n")
            phishing_URLs.extend(url)

    return phishing_URLs


def clear_duplicates(phishing_URLs):

    no_duplicates = []  # Contains links with unique domains
    # Contains domains of links, that are already included in no_duplicates
    # list
    seen_domains = []
    for URL in phishing_URLs:

        domain = find_domain(URL)
        if domain not in seen_domains:
            no_duplicates.append(URL)
            seen_domains.append(domain)

    return no_duplicates

# Extracts the domain part of the url


def find_domain(link):

    # Replace common url parts
    link = re.sub("|".join(['www.', 'https://', 'http://', '\n']), "", link)
    domain = re.search('[^/]*', link).group(0)

    return domain


def save_data(phishing_URLs):
    with open('data/new_phishing_urls.dat', 'a+') as f:
        for url in phishing_URLs:
            f.write(url + "\n")

    print(" Phishing urls saved at the location: data/new_phishing_urls.dat")
    f.close()


if __name__ == '__main__':

    phishing_URLs = download_phishing_data()
    phishing_URLs = clear_duplicates(phishing_URLs)
    save_data(phishing_URLs)
