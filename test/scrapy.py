import urllib.request
from bs4 import BeautifulSoup

header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
}
url = "http://www.sina.com"

request = urllib.request.Request(url=url, headers=header)  # url为爬取的链接，headers主要是假装我们不是爬虫，现在我们就假装我们是个Chrome浏览器

response = urllib.request.urlopen(request)  # 请求数据

data = response.read()  # 读取返回的数据

data.decode("UTF-8")  # 设置字符格式为utf-8，可以处理中文

soup = BeautifulSoup(data, "html.parser")  # 把html转换成BeautifulSoup对象，这样我们就可以用BeautifulSoup的方法来解析html

print(soup.title)  # 打印标题

print(soup.find_all("a"))  # 打印所有a标签







