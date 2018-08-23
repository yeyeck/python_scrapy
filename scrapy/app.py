import urllib.request
from bs4 import BeautifulSoup

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}


# 因为有时候得到的是一段 json 或者别的数据，有时候是html，所以我们单纯地先获取数据
def get_data(url, headers=header, charset="unicode", errors="ignore"):
    req = urllib.request.Request(url=url, headers=headers)
    rep = urllib.request.urlopen(req)
    data = rep.read()
    return data.decode(charset, errors)


# 如果是个html我们就可以用BeautifulSoup解析
def get_soup(url, headers=header, charset="utf-8"):
    data = get_data(url=url, headers=headers, charset=charset)
    return BeautifulSoup(data, "html.parser")












