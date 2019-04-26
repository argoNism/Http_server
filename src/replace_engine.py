import re
from datetime import datetime
import sys
import os
import errors
import articles
import sqlite3

class TemplateEngine:

    title_pat = r'%title\((.*)\)'
    body_pat = r'%body\((.*|<br>)\)'

    patterns = {
        '%(time-stamp)': datetime.now().strftime("%Y/%m/%d"),
        '%(title)': '',
        '%(body)': '',
    }

    methods = {
        '%font(\d+)\((.*)\)'
    }

    def __init__(self, template: str, pairs: str):
        self.pairs = pairs
        self.template = template
        
    # htmlのソースコードをstrで返す
    def render(self):
        try:
            result = self.template

            self.init()

            for k, v in self.pairs.items():
                result = result.replace(k, v)

            return result
        except:
            raise errors.TemplateRenderingError("Fail to replaces.")

# def main():
#     with open("../template/input.txt") as f:
#                 input_file = f.read()
    
#     title = re.search(r'%title\((.*)\)', input_file).group(1) if re.search(r'%title\((.*)\)', input_file) else ''
#     body = re.search(r'%body\((.*|<br>)\)', input_file).group(1) if re.search(r'%body\((.*|<br>)\)', input_file) else ''

#     article = articles.Article(title, body, [], "4-24")

#     temp = TemplateEngine(article, "template")
#     print(temp.render())


# if __name__ == "__main__":
#     main()

def render(template, pairs):
    try:
        result = template

        for k, v in pairs.items():
            result = result.replace(k, v)

        return result
    except:
        raise errors.TemplateRenderingError("Fail to replaces.")

def set_latest(template, count=5):
    style = '<li><a href="#"><i class="fas fa-angle-right"></i>頭が痒くない今日この頃</a></li>'
    
    conn = sqlite3.connect("../db/articles.db")
    c = conn.cursor()
    c.execute("select * form articles order by ")
    template = template.replace(%(latest), )

if __name__ == "__main__":
    pairs = {
        '%(time-stamp)': datetime.now().strftime("%Y/%m/%d"),
        '%(title)': 'タイトルのテストfrom replace_engine',
        '%(body)': 'ボディのテスト',
    }

    with open("../template/template.html") as file:
        print(render(file.read(), pairs))