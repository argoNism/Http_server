import sqlite3
import re
from datetime import datetime

#
#実装していくもの:
#   データベースに記事を登録
#   データベースから記事情報を列単位で取り出す。
#   データベースから記事の検索。結果の取り出し。
#   タグの管理。


class Article:
    def __init__(self, title: str, body: str, tags: list, time: str):
        self.title = title
        self.body = body
        self.tags = []
        self.time = time

    def tag(self):
        pass

#　Articleオブジェクトを受け取って、データベースに追加する。
def add_article(article: Article):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        c.execute("insert into article (title, body, time) values (?,?,?)", (article.title, article.body, datetime.now().strftime("%Y/%m/%d")))
        conn.commit()
        print("save article", (article.title, article.body, datetime.now().strftime("%Y/%m/%d")))

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

def add_tag(str):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        c.execute("insert into tags(name) values (?)", (str))
        conn.commit()
        print("add tags:", str)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

# get articles from database. count var is number of row. if count is under 0, return all results.
# if you set title, you can get one article.
def get_articles(title="", count=0) -> list:
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        if title:
            c.execute("select * from articles where title = ?", (title))
            # リストの〇番目にまとまってる
            result = c.fetchall()
            result = result[0]
            
            article = article.Article()
            article.title = result[1]
            article.body = result[2]
            article.time =  result[3]

            return article

        else:
            if count <= 0:
                c.execute("select * from articles")
            else:
                c.execute("select * from articles limit ?", (count))
            return c.fetchall()

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)
        return []
        

# get article titles (and id by default) from database.
def get_titles(with_id=True):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        if with_id:
	        c.execute("select id, title from articles")
        else:
	        c.execute("select title from articles")
        
        return c.fetchall()

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

        return []
