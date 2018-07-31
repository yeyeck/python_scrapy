import urllib.request
from bs4 import BeautifulSoup

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
}


def get_soup(url, headers):
    req = urllib.request.Request(url=url, headers=headers)
    rep = urllib.request.urlopen(req)
    page_data = rep.read().decode("UTF-8")
    soup = BeautifulSoup(page_data, "html.parser")
    return soup


def scrap(url, headers):
    soup = get_soup(url, headers)
    return soup


s = scrap("http://www.sina.com", header)
print(s)





