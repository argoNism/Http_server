import re
from datetime import datetime
import sys
import os
import errors

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

    def __init__(self, body: str, template_name):
        self.body = body
        self.template_name = template_name
        

    def get_template(self, template_name):
        try:
            if os.path.exists("template/" + template_name + ".html"):
                with open("template/" + template_name + ".html") as f:
                    return f.read()
            else:
                raise errors.GetTemplateError("There is no such a" + template_name)

        except errors.GetTemplateError as e:
            raise e
        except:
            raise errors.GetTemplateError("Fail to read template file")
        

    def render(self):
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
            raise errors.TemplateRenderingError("fail to render template")


    def init(self):
        with open("template/input.txt") as f:
                input_file = f.read()

        with open("template/body.txt") as f:
            body_txt = f.read()

        body_txt = re.sub('\n', '<br>', body_txt)

        input_file = re.sub('\"body\"', body_txt, input_file)

        # matchとsearchの使い分けに注意
        self.patterns['%(title)'] = re.search(self.title_pat, input_file).group(1) if re.search(self.title_pat, input_file) else ''
        self.patterns['%(body)'] = re.search(self.body_pat, input_file).group(1) if re.search(self.body_pat, input_file) else ''

        print(self.patterns)

def main():
    args = sys.argv

    temp = TemplateEngine("", "template_page")

    with open("www/" + args[1] + ".html", mode='w') as file:
        file.write(temp.render())


if __name__ == "__main__":
    main()
