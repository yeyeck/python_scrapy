# import urllib.request
# from bs4 import BeautifulSoup


#
# url = ("https://btshow.jd.com/queryBtPlanInfo.do?callback=queryBtPlanInfo&sku=10671563387&cId=1315%2C1343%2C9719"
#        "&num=1&amount=59&sourceType=PC-XQ&shopId=169317&ver=1&areaId=1&isJd=true&_=1533127714744")
#
# request = urllib.request.Request(url=url, headers=header)  # url为爬取的链接，headers主要是假装我们不是爬虫，现在我们就假装我们是个Chrome浏览器
#
# response = urllib.request.urlopen(request)  # 请求数据
#
# data = response.read()  # 读取返回的数据
#
# data.decode("UTF-8")  # 设置字符格式为utf-8，可以处理中文
#
# print(data)
#
# soup = BeautifulSoup(data, "html.parser")  # 把html转换成BeautifulSoup对象，这样我们就可以用BeautifulSoup的方法来解析html
#
# print(soup.title)  # 打印标题
#
# print(soup.find_all("a"))  # 打印所有a标签


# import scrapy
#
# header = {
#     'User-Agent':
#         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
#     'Referer': 'https://item.jd.com/24146604746.html'
#
# }
# url = "https://btshow.jd.com/queryBtPlanInfo.do?callback=queryBtPlanInfo&sku=24146604746&cId=1315%2C1343%2C9719&isJd=true&_=1533378852175"
#
# print(scrapy)

def sumSubseqWidths(A):
    """
    :type A: List[int]
    :rtype: int
    """
    re = []
    le = len(A)
    for i in range(le+1):
        for j in range(i):
            sub = A[j:i]
            re.append(max(sub) - min(sub))
    return sum(re)


A = [2, 1, 3]
res = sumSubseqWidths(A)
print(res)









