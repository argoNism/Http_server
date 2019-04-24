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
    def __init__(self, title: str, body: str, tags: list, time=""):
        self.title = title
        self.body = body
        self.tags = []
        self.time = time

    def tag(self):
        pass


def map_tags(article_id: int, tags_name: list):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        found_tag_id = []
        for name in tags_name:
            c.execute("select id from tags where name = (?)", (name))
            tag_id = c.fetchall()
            if tag_id:
                found_tag_id.append(tag_id)
            else:
                c.execute("insert into tags(name) values (?)", (name))
                conn.commit()
                c.execute("select id from tags where name = (?)", (name))
                found_tag_id.append(c.fetchall())
        
        for id in found_tag_id:
            c.execute("insert into tag_maps(target_id, tag_id) values(?, ?)", (article_id, id))
            c.commit()

        print("map tags:", article_id, tags_name)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


#　Articleオブジェクトを受け取って、データベースに追加する。
def add_article(article: Article):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        c.execute("insert into articles (title, body, time) values (?,?,?)", (article.title, article.body, datetime.now().strftime("%Y/%m/%d")))
        c.commit()
        c.execute("select id from articles where title = ?", (article.title))
        map_tags(c.fetchone(), article.tags)
        print("save article", (article.title, article.body, datetime.now().strftime("%Y/%m/%d")))

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


def add_tag(tag_name):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        c.execute("insert into tags(name) values (?)", (tag_name))
        conn.commit()
        print("add tags:", tag_name)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


def get_tags(article_id: int):
    try:
        conn = sqlite3.connect('db/articles.db')
        c = conn.cursor()
        c.execute("select tag_id from tag_maps where target_id = ?", (article_id))
        id_list = c.fetchall()
        tag_names = []
        for id in id_list:
            c.execute("select name from tagss where id = ?", (id))
            tag_names.append(c.fetchone())
        
        return tag_names

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

        return []


# get articles from database. count var is number of row. if count is under 0, return all results.
# if you set title, you can get one article.
def get_articles(title="", count=0) -> Article:
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

            # タグを取得
            article.tags = get_tags(result[0])

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
