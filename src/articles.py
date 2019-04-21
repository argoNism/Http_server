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
    pass


