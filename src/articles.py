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

    def body_for_html(self):
        result = re.sub(r'\n', "<br>", self.body)
        print("body_for_html:", result)
        return result

# タイトルから、対応する記事と、タグマップを削除する
def delete_article(title="", id=None):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        if not id and title:
            c.execute("select * from articles where title = (?)", (title,))
            article = c.fetchone()
            if article:
                target_id = article[0]
            else:
                print("There is no such title article:", title)
                return

        elif not title:
            print("need title name or article id")
            return
        
        c.execute("delete from tag_maps where target_id = (?)", (target_id,))
        c.execute("delete from articles where id = (?)", (target_id,))
        conn.commit()
        print("delete article:", title)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


def add_tag(tag_name):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        c.execute("insert into tags(name) values (?)", (tag_name,))
        conn.commit()
        print("add tags:", tag_name)

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)

# 登録されてるタグのリストを取得
def get_tag_list():
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        c.execute("select name from tags")
        name_list = []
        for name in c.fetchall():
            name_list.append(name[0])
        return name_list

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


# 特定の記事にマップされてるタグを取得する
def get_tags(article_id):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        c.execute("select tag_id from tag_maps where target_id = (?)", (str(article_id),))
        c.execute("select tags.name from tags left outer join tag_maps on tags.id = tag_maps.tag_id where tag_maps.target_id = (?)", (str(article_id),))
        # 戻り値の例: [('VPS',), ('blog',), ('ゲーム',)]
        result = c.fetchall()
        # id_list = c.fetchall()
        # tag_names = []
        # for id in id_list:
        #     c.execute("select name from tags where id = (?)", (str(id),))
        #     tag_names.append(c.fetchone())
        
        # return tag_names
        print("get tags:", result)
        return result

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
            c.execute("select * from articles where title = (?)", (title,))
            # リストの〇番目にまとまってる
            result = c.fetchall()
            if result:
                result = result[0]
                article = Article(title, result[2], get_tags(result[0]), created_at=result[3], updated_at=result[4])
                return article
            else:
                return
        else:
            if count <= 0:
                c.execute("select * from articles")
                article_list = c.fetchall()

            else:
                c.execute("select * from articles limit (?)", (str(count),))
            
                article_list = []
                for collum in c.fetchall():
                    article = Article(collum[1], collum[2], get_tags(collum[0]), created_at=collum[3], updated_at=collum[4])
                    article_list.append(article)

            return article_list

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

# add relation between article and tags. If tag is not existed, you can chose add the tag or not.
# 記事とタグをマップする。存在しないタグなら、追加するか確認する。追加しないなら、そのタグは無視される
def map_tags(article_id: int, tags_name: list):
    try:
        conn = sqlite3.connect(DATABASE_ROOT + 'articles.db')
        c = conn.cursor()
        found_tag_id = []
        maped_tags_name = []
        for name in tags_name:
            c.execute("select id from tags where name = (?)", (name,))
            tag_id = c.fetchone()
            if tag_id:
                found_tag_id.append(tag_id[0])
            else:
                print("There is no such tag. Do you want add", name, " in tags? Y/N")
                get = input()
                if get in ('Y', 'y', 'yes', 'Yes', 'YES'):
                    add_tag(name)
                    c.execute("select id from tags where name = (?)", (name,))
                    id = c.fetchone()
                    found_tag_id.append(id[0])
                    maped_tags_name.append(name)
                else:
                    continue
        
        for id in found_tag_id:
            c.execute("insert into tag_maps(target_id, tag_id) values(?, ?)", (article_id[0], id))
            conn.commit()

        print("map tags:", article_id[0], tags_name)

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
            c.execute("select id from articles where title = ?", (article.title,))
            map_tags(c.fetchone(), article.tags)

        print("save article", (article.title, article.body, article.tags))

    except sqlite3.OperationalError as e:
        print("sqlite3.OperationalError:", e)


if __name__ == "__main__":
    pass