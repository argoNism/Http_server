import re
from datetime import datetime
import sys
import os
import errors
import articles
import replace_engine
import main

class TemplateEngine:

    title_pat = r'%title\((.*)\)'
    body_pat = r'%body\((.*|<br>)\)'

    patterns = {
        '%(time-stamp)': '',
        '%(title)': '',
        '%(body)': '',
    }

    methods = {
        '%font(\d+)\((.*)\)'
    }

    def __init__(self, article: articles.Article, template_name="", partial_temp=""):
        self.article = article
        self.template_name = template_name
        self.patial_temp = partial_temp
        

    def get_template(self, template_name):
        try:
            if os.path.exists(main.DOCUMENT_ROOT + "/../template/" + template_name + ".html"):
                with open(main.DOCUMENT_ROOT + "/../template/" + template_name + ".html") as f:
                    return f.read()
            else:
                print(main.DOCUMENT_ROOT + "/../template/" + template_name + ".html")
                raise errors.GetTemplateError("There is no such a " + template_name)

        except errors.GetTemplateError as e:
            raise e
        # except:
        #     raise errors.GetTemplateError("Fail to read template file.")
        
    # htmlのソースコードをstrで返す
    def render(self):
        # to get template
        try:
            if self.template_name:
                self.template = self.get_template(self.template_name)
            else:
                self.template = self.patial_temp

        except errors.GetTemplateError as e:
            print(e)
            raise e

        result = self.set_template_assigns(self.template)

        self.init_pattern()

        for k, v in self.patterns.items():
            print(k, v)
            result = result.replace(k, v)

        return result

        # try:
            
        # except:
        #     raise errors.TemplateRenderingError("Fail to render template.")

    def init_pattern(self):
        # matchとsearchの使い分けに注意
        self.patterns['%(time-stamp)'] = self.article.created_at
        self.patterns['%(title)'] = self.article.title
        self.patterns['%(body)'] = self.article.body

        print(self.patterns)

    def set_template_assigns(self, template):
        result = replace_engine.set_latest(template)
        result = replace_engine.set_tags(result, self.article.tags)
        return result


# def main():
#     with open("../template/input.txt") as f:
#                 input_file = f.read()
    
#     title = re.search(r'%title\((.*)\)', input_file).group(1) if re.search(r'%title\((.*)\)', input_file) else ''
#     body = re.search(r'%body\((.*|<br>)\)', input_file).group(1) if re.search(r'%body\((.*|<br>)\)', input_file) else ''

#     article = articles.Article(title, body, [], "4-24")

#     temp = TemplateEngine(article, "template")
#     print(temp.render())


# if __name__ == "__main__":
#     article = articles.Article("タイトルの2", "ぼでーの1", ["aaa", "C#", "プログラミング", "強プロ"], created_at="000000")
#     print(len(article.tags))
#     temp = TemplateEngine(article, "template")
#     print(temp.render())
