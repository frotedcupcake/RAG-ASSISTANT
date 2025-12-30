import requests
from bs4 import BeautifulSoup

def load_web(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(separator="\n")
    return text
