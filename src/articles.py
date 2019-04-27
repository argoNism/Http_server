import sqlite3
import re
from datetime import datetime

#
#実装していくもの:
#   データベースに記事を登録
#   データベースから記事情報を列単位で取り出す。
#   データベースから記事の検索。結果の取り出し。
#   タグの管理。

DATABASE_ROOT = "../db/"

class Article:
    def __init__(self, title: str, body: str, tags: list, created_at="", updated_at=""):
        self.title = title
        self.body = body
        self.tags = tags
        self.created_at = created_at
        self.updated_at = updated_at


def add_tag(tag_name):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        c.execute("insert into tags(name) values (?)", (tag_name))
        conn.commit()
        print("add tags:", tag_name)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


def get_tags(article_id: int):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        print(type(article_id))
        c.execute("select tag_id from tag_maps where target_id = ?", (str(article_id)))
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
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        if title:
            print("article title:", title)
            c.execute("select * from articles where title = ?", (title,))
            # リストの〇番目にまとまってる
            result = c.fetchall()
            result = result[0]
            
            article = Article(title, result[2], get_tags(result[0]), created_at=result[3], updated_at=result[4])

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
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        if with_id:
	        c.execute("select id, title from articles")
        else:
	        c.execute("select title from articles")
        
        return c.fetchall()

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

        return []


def map_tags(article_id: int, tags_name: list):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        found_tag_id = []
        maped_tags_name = []
        for name in tags_name:
            c.execute("select id from tags where name = (?)", (name))
            tag_id = c.fetchall()
            if tag_id:
                found_tag_id.append(tag_id)
            else:
                print("There is no such tag. Do you want add", name, " in tags? Y/N")
                get = input()
                if get in ('Y', 'y', 'yes', 'Yes', 'YES'):
                    add_tag(name)
                    c.execute("select id from tags where name = (?)", (name))
                    found_tag_id.append(c.fetchall())
                    maped_tags_name.append(name)
                else:
                    continue
        
        for id in found_tag_id:
            c.execute("insert into tag_maps(target_id, tag_id) values(?, ?)", (article_id, id))
            conn.commit()

        print("map tags:", article_id, tags_name)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


#　Articleオブジェクトを受け取って、データベースに追加する。
def add_article(article: Article):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        # c.execute("select * from sqlite_master where type='table'")
        # print(c.fetchone())
        try:
            c.execute("insert into articles(title, body, created_at, updated_at) values (?,?, datetime('now', 'localtime'), datetime('now', 'localtime'))", (article.title, article.body))
            conn.commit()
        except sqlite3.IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: articles.title':
                print("タイトルは既に登録されています！別のタイトルを入力してください。")
            return

        if article.tags:
            c.execute("select id from articles where title = ?", (article.title))
            map_tags(c.fetchone(), article.tags)

        print("save article", (article.title, article.body))

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


# if __name__ == "__main__":
#     for i in range(1, 10):
#         title = "タイトル" + str(i)
#         body = "ぼでー" + str(i)
#         article = Article(title, body, tags=[])
#         add_article(article)
