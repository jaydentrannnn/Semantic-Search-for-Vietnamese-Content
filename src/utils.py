import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import unicodedata
from urllib.parse import urljoin

from config import CONTENT_TAGS  # fixed import



def get_soup(url):
    #Get url contents and return it as a soup object
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')



def clean_soup(soup):
    #clean up the style and script in the soup
    for script_and_style in soup(["script", "style"]):
        script_and_style.decompose()
    return soup.find(id="mw-content-text")



def get_h3_and_content(soup):
    #Get all the h3 and there contents
    h3_tags = soup.find_all('h3')
    h3_tags_to_contents_map = defaultdict(list)

    for h3 in h3_tags:
        h3_text = h3.get_text(strip=True)
        if not h3_text:
            continue
        content = []
        element = h3
        while True:
            element = element.find_next()
            if not element or element.name in ('h2', 'h3'):
                break
            if element.name in CONTENT_TAGS:
                content.append(element.get_text(strip=True, separator=" "))
        h3_tags_to_contents_map[h3_text].append(' '.join(content))

    return h3_tags_to_contents_map



def normalize(text: str):
    #Normalize the text
    text = text.lower()
    text = unicodedata.normalize('NFC', text)
    return re.sub(r'\s+', ' ', text).strip()



def get_all_hyperlinks(url):
    #Get all the hyperlink from the page
    soup = get_soup(url)
    all_hyperlinks = []
    for link in soup.find_all('a', href=True):
        absolute_link = urljoin(url, link['href'])
        all_hyperlinks.append(absolute_link)
    return all_hyperlinks
