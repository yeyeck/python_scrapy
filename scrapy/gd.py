from scrapy import app
import re


header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    # 'Referer': 'https://item.jd.com/10671563387.html'

}

url = "https://item.jd.com/27934623028.html"
soup = app.get_soup(url=url, charset="gbk")   # 获取BeautifulSoup对象

pid = re.search("[0-9]+", url).group()    # 用正则筛选id
print("商品id：", pid)

title = soup.find("div", class_="sku-name").string.strip()   # 爬商品名称
print("商品名称：", title)

page_config = soup.find("script", {"charset": "gbk"}).string
cat = re.search("(?<=cat:\s\[)[,0-9]*(?=\])", page_config).group()   # 用正则匹配到商品类目

print("category: ", cat)


stock_url = ("https://c0.3.cn/stock?skuId=27934623028&area=1_72_2799_0&venderId=137483&cat={1}"
             "&buyNum=1&choseSuitSkuIds=&extraParam={%22originid%22:%221%22}&ch=1&fqsp=0"
             "&pdpin=&detailedAdd=null&callback=jQuery3539584").format(pid, cat)
print(app.get_data(url=stock_url, charset="gbk"))




