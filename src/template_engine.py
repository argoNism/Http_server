import re
from datetime import datetime
import sys
import os
import errors
import articles

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

    def __init__(self, article: articles.Article, template_name):
        self.article = article
        self.template_name = template_name
        

    def get_template(self, template_name):
        try:
            if os.path.exists("../template/" + template_name + ".html"):
                with open("../template/" + template_name + ".html") as f:
                    return f.read()
            else:
                raise errors.GetTemplateError("There is no such a " + template_name)

        except errors.GetTemplateError as e:
            raise e
        except:
            raise errors.GetTemplateError("Fail to read template file.")
        
    # htmlのソースコードをstrで返す
    def render(self):
        # to get template
        try:
            self.template = self.get_template(self.template_name)
        except errors.GetTemplateError as e:
            print(e)
            raise e

        try:
            result = self.template

            self.init()

            for k, v in self.patterns.items():
                result = result.replace(k, v)

            return result
        except:
            raise errors.TemplateRenderingError("Fail to render template.")

    # 置き換える文字を抽出する（エディた実装後は不要のはず（個別に受け取ることがぜんていになるから。）
    def init(self):
        # matchとsearchの使い分けに注意
        self.patterns['%(title)'] = self.article.title
        self.patterns['%(body)'] = self.article.body

        print(self.patterns)

def main():
    with open("../template/input.txt") as f:
                input_file = f.read()
    
    title = re.search(r'%title\((.*)\)', input_file).group(1) if re.search(r'%title\((.*)\)', input_file) else ''
    body = re.search(r'%body\((.*|<br>)\)', input_file).group(1) if re.search(r'%body\((.*|<br>)\)', input_file) else ''

    article = articles.Article(title, body, [], "4-24")

    temp = TemplateEngine(article, "template")
    print(temp.render())


if __name__ == "__main__":
    main()
