import os
import urllib.parse
import main
from response import Response
import content_type
from http_state import States
import articles
from template_engine import TemplateEngine
import replace_engine
utf8_map =[
    "html", "css", "plane", "javascript"
]

rb_map = [
    "png", "jpeg", "jpeg", "gif", "vnd.microsoft.icon"
]

class BaseController:

    def __init__(self):
        pass

    #GETメソッドを受け取った時
    def do_get(self, request) -> Response:
        self.path: str = urllib.parse.unquote(request.target)
        self.root, self.ext = os.path.splitext(self.path)
        self.ext = self.ext.lstrip(".")

        self.path = self.format_path(self.path)

    def do_post(self, request) -> Response:
        self.path: str = urllib.parse.unquote(request.target)
        self.root, self.ext = os.path.splitext(self.path)
        self.path = self.format_path(self.path)

    def format_path(self, path) -> str:
        #ディレクトリトラバーサル対策
        if (not path.find("..") == -1):
            path = "index.html"

        if (path.endswith("/")):
            path = path = path.rstrip("/")


            # 受け取ったpath
        if (path.startswith("/")):
            path = path.lstrip("/")

        return path
    
    def open_files(self, path, ext: str):
        if ext in utf8_map:
            with open(path, encoding='utf-8') as file:
                return file.read()

        elif ext in rb_map:
            with open(path, mode='rb') as file:
                return file.read()

        else:
            with open(path, encoding='utf-8') as file:
                return file.read()

    def not_found(self):
        # self.path = self.path.rstrip("/") if self.path.endswith("/") else self.path
        self.response = Response(main.protocolVersion, States.Not_Found)
        self.response.body = self.open_files(os.path.join(main.DOCUMENT_ROOT, "not_found.html"), "html")
        self.ext = "html"

        return self.response


class NormalController(BaseController):

    def __init__(self):
        pass

    #GETメソッドを受け取った時
    def do_get(self, request) -> Response:
        super().do_get(request)

        # make responce object so determine states code
        #指定されたuriのファイルが存在するか確認
        if os.path.exists(os.path.join(main.DOCUMENT_ROOT, self.path)) and os.path.isfile(os.path.join(main.DOCUMENT_ROOT, self.path)):
            self.response = Response(main.protocolVersion, States.OK)
            self.response.body = self.open_files(os.path.join(main.DOCUMENT_ROOT, self.path) ,self.ext)

        #ファイルが見つからない時、not_found.htmlを送信
        else:
            self.response = self.not_found()
            
        self.response.add_header("Content-Type", content_type.get_content_text(self.ext))

        return self.response


class ArticleController(BaseController):
    def __init__(self):
        pass
    
    def do_get(self, request):
        super().do_get(request)
        # print("self.path", self.path)
        # if self.path in ["blog", "blog/", "/", ""]:
        #     self.response = Response(main.protocolVersion, States.OK)
        #     self.response.body = replace_engine.set_top_page(main.DOCUMENT_ROOT + "/blog_top.html")
        #     self.ext = "html"

        #     return self.response

        head, tail = os.path.split(self.path)
        print("tail",tail)
        if tail and not tail == "blog":
            print("in article")
            article = articles.get_articles(tail)

            if article:
                engine = TemplateEngine(article, "template")
                self.response = Response(main.protocolVersion, States.OK)
                self.response.body = engine.render()
                self.ext = "html"

            else:
                self.response = self.not_found()

        else:
            print("in blog_top")
            self.response = Response(main.protocolVersion, States.OK)
            self.response.body = replace_engine.set_top_page(main.DOCUMENT_ROOT + "/blog_top.html")
            self.ext = "html"

            return self.response
            # self.response = Response(main.protocolVersion, States.Not_Found)
            # self.response.body = os.path.join(main.DOCUMENT_ROOT, "blog.html")
            # self.ext = "html"

        return self.response

    def do_post(self, request):
        super().do_post(request)
        print("self.path", self.path)
        if self.path == "blog/post":
            print("blog/post")
            print("request body:", request.body)
        tags = request.body["tags"].split(",")
        article = articles.Article(request.body["title"], request.body["body"], tags)
        articles.add_article(article)


class AdminController():

    def __init__(self):
        pass

    #GETメソッドを受け取った時
    def do_post(self, request) -> Response:
        pass


# class BlogController(BaseController):
#     def __init__(self):
#         pass
    
#     def do_get(self, request):
#         super().do_get(request)
#         head, tail = os.path.split(self.path)
#         if tail:
#             article = articles.get_articles(tail)

#             if article:
#                 engine = TemplateEngine(article, "template")
#                 self.response = Response(main.protocolVersion, States.OK)
#                 self.response.body = engine.render()

#             else:
#                 self.response = self.not_found()

#         else:
#             self.response = Response(main.protocolVersion, States.Not_Found)
#             self.response.body = os.path.join(main.DOCUMENT_ROOT, "blog.html")
#             self.ext = "html"


#         return self.response
