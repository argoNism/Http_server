import re
from datetime import datetime
import sys
import os
import errors
import articles
import sqlite3
import template_engine
import main

# class TemplateEngine:

#     title_pat = r'%title\((.*)\)'
#     body_pat = r'%body\((.*|<br>)\)'

#     patterns = {
#         '%(time-stamp)': datetime.now().strftime("%Y/%m/%d"),
#         '%(title)': '',
#         '%(body)': '',
#     }

#     methods = {
#         '%font(\d+)\((.*)\)'
#     }

#     def __init__(self, template: str, pairs: str):
#         self.pairs = pairs
#         self.template = template
        
#     # htmlのソースコードをstrで返す
#     def render(self):
#         try:
#             result = self.template

#             self.init()

#             for k, v in self.pairs.items():
#                 result = result.replace(k, v)

#             return result
#         except:
#             raise errors.TemplateRenderingError("Fail to replaces.")

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
    result = template

    for k, v in pairs.items():
        result = result.replace(k, v)

    return result
    # try:
    #     result = template

    #     for k, v in pairs.items():
    #         result = result.replace(k, v)

    #     return result
    # except:
    #     raise errors.TemplateRenderingError("Fail to replaces.")

def set_latest(template, count=5):
    print("set_latest")
    style = '<li><a href="%(link)"><i class="fas fa-angle-right"></i>%(title)</a></li>'
    print("open:", main.DOCUMENT_ROOT + "/../db/articles.db")
    conn = sqlite3.connect(main.DOCUMENT_ROOT + "/../db/articles.db")
    c = conn.cursor()
    c.execute("select * from articles order by created_at limit ?", (str(count)))
    li_list = ""
    # c.fetchall() -> 一つの要素が、カラムになってるリスト
    for column in c.fetchall():
        temp = style.replace("%(title)", column[1])
        temp = temp.replace("%(link)", "/blog/" + column[1])
        li_list += (temp + '\n')

    return template.replace("%(latest)", li_list)

def set_tags(template, tags):
    style = '<li>%(tag)</li>'
    li_list = ""
    for tag in tags:
        temp = style.replace("%(tag)", tag[0])
        li_list += (temp + '\n')

    return template.replace("%(tags)", li_list)

def set_top_page(url):
    template_long = '<li>'\
                        '<article>'\
                            '<div class="container">'\
                                '<p class="time-stamp">%(time-stamp)</p>'\
                                '<ul class="tags">'\
                                    '%(tags)'\
                                '</ul>'\
                                '<h2><i class="fas fa-square-full"></i>%(title)</h2>'\
                                '<p class="article">%(body)</p>'\
                                '<a class="continue" href="blog/%(title)"><i class="fas fa-angle-right"></i>続きを読む</a>'\
                            '</div>'\
                        '</article>'\
                    '</li>'
            
    with open(url) as file:
        base = file.read()

    article_list = articles.get_articles(count=10)
    rendered = ""
    for arti in article_list:
        patterns = {}
        if len(arti.body) > 50:
            arti.body = arti.body[:50]
            arti.body += "..."
        # engine = template_engine.TemplateEngine(arti, partial_temp=template_long)
        patterns['%(time-stamp)'] = arti.created_at
        patterns['%(title)'] = arti.title
        patterns['%(body)'] = arti.body_for_html()
        rendered += render(template_long, patterns)
        rendered = set_tags(rendered, arti.tags)

        # rendered += engine.render() + "\n"
    rendered = render(base, {"%(article)": rendered})
    rendered = set_latest(rendered)

    return rendered



        


# if __name__ == "__main__":
#     with open("../template/template.html") as file:
#         print(set_latest(file.read()))
        
    # pairs = {
    #     '%(time-stamp)': datetime.now().strftime("%Y/%m/%d"),
    #     '%(title)': 'タイトルのテストfrom replace_engine',
    #     '%(body)': 'ボディのテスト',
    # }

    # with open("../template/template.html") as file:
    #     print(render(file.read(), pairs))