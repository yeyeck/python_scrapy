from scrapy import app
import re
import datetime
import pymysql


def douban_movie(movie_url):

    header = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Host': 'movie.douban.com',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    movie = {}

    m_id = re.search("[0-9]+", movie_url).group()
    movie["id"] = int(m_id)
    # 获取soup对象
    soup = app.get_soup(url=movie_url, headers=header, charset="utf-8")
    content = soup.find(id="content")

    kinds = content.find(class_="episode_list")
    movie["type"] = 0 if kinds else 1             # 0 ：电视剧，1：电影。如果有分集数，为电视剧， 否则就是电影
    # 抓取电影名字和上映年份
    m_name = content.find("h1").find("span").string
    movie["name"] = m_name;
    m_year = content.find(class_="year").string
    m_year = m_year[1:-1]  # 去掉头尾的括号
    movie["year"] = m_year
    # 抓取导演
    info = content.find(id="info")
    m_directer = info.find(attrs={"rel": "v:directedBy"}).string
    movie["directer"] = m_directer
    # 上映日期
    m_date = info.find(attrs={"property": "v:initialReleaseDate"}).string
    m_date = re.search("[-,0-9]+", m_date).group()
    movie["date"] = datetime.datetime.strptime(m_date, '%Y-%m-%d')

    # 类型
    categories = info.find_all(attrs={"property": "v:genre"}, limit=2)
    m_categories = []
    for category in categories:
        m_categories.append(category.string)
    movie["categories"] = m_categories

    # 抓取主演，只取前面五个
    actors = info.find(class_="actor").find_all(attrs={"rel": "v:starring"}, limit=5)
    m_actors = []
    for actor in actors:
        m_actors.append(actor.string)
    movie["actors"] = m_actors
    # 片长
    m_time = info.find(attrs={"property": "v:runtime"})
    m_time = int(re.search("[0-9]+", m_time.string).group()) if m_time else 0
    movie["time"] = m_time
    # 评分
    score_info = soup.find(id="interest_sectl")
    m_score = score_info.find("strong").string if score_info.find("strong") else 0.0
    movie["score"] = float(m_score) if m_score else 0.0
    m_stars = score_info.find_all(class_="rating_per")
    m_rate = []
    for star in m_stars:
        m_rate.append(float(star.string[:-1]))
    movie["stars"] = m_rate
    m_votes = score_info.find(attrs={"property": "v:votes"})
    m_votes = int(m_votes.string) if m_votes else 0
    movie["vote"] = m_votes
    return movie


def inset_data(movie):
    # 获取一个数据库连接
    conn = pymysql.Connect(host="localhost", port=3306, user="root", password="root", db="douban")
    # conn.autocommit(True)    # 设置自动提交
    cursor = conn.cursor()   # 获取游标
    sql_insert_info = ("insert into `t_movie_info`(`id`, `type`, `name`, `director`, `year`, `month`, `day`, "
                       "`categories1`, `categories2`, `time`) values (%d, %d, '%s', '%s', %d, %d, %d, '%s', '%s', %d)")

    categories = movie["categories"]
    ca_len = len(categories)
    categories1 = categories[0] if ca_len > 0 else None
    categories2 = categories[1] if ca_len > 1 else None

    cursor.execute(sql_insert_info % (movie["id"], movie["type"], movie["name"], movie["directer"], movie["date"].year,
                                      movie["date"].month, movie["date"].day, categories1, categories2, movie["time"]))

    # 写sql 千万记住 %s 要加双引号，不然会报错 Unknown column 'a' in 'field list'
    sql_insert_actors = ("insert into `t_movie_actors`(id, actor1, actor2, actor3, actor4, actor5)"
                         "values(%d, '%s', '%s', '%s', '%s', '%s')")
    actors = movie["actors"]
    actors_len = len(actors)
    actor1 = actors[0] if actors_len > 0 else None
    actor2 = actors[1] if actors_len > 1 else None
    actor3 = actors[2] if actors_len > 2 else None
    actor4 = actors[3] if actors_len > 3 else None
    actor5 = actors[4] if actors_len > 4 else None

    cursor.execute(sql_insert_actors % (movie["id"], actor1, actor2, actor3, actor4, actor5))

    sql_insert_scores = ("insert into `t_movie_scores`(id, score, votes, star1, star2, star3, star4, star5)"
                         "values(%d, %f, %d, %f, %f, %f, %f, %f)")
    stars = movie["stars"]
    stars_len = len(stars)
    star1 = stars[0] if stars_len > 0 else 0.0
    star2 = stars[1] if stars_len > 1 else 0.0
    star3 = stars[2] if stars_len > 2 else 0.0
    star4 = stars[3] if stars_len > 3 else 0.0
    star5 = stars[4] if stars_len > 4 else 0.0
    cursor.execute(sql_insert_scores % (movie["id"], movie["score"], movie["vote"], star1, star2, star3, star4, star5))
    conn.commit()


data1 = douban_movie("https://movie.douban.com/subject/30236775/?from=showing")
inset_data(data1)
data2 = douban_movie("https://movie.douban.com/subject/26842702/?tag=%E7%83%AD%E9%97%A8&from=gaia")
inset_data(data2)
data3 = douban_movie("https://movie.douban.com/subject/26973784/?tag=%E6%9C%80%E6%96%B0&from=gaia")
inset_data(data3)
data4 = douban_movie("https://movie.douban.com/subject/30249296/?tag=%E7%83%AD%E9%97%A8&from=gaia")
inset_data(data4)







