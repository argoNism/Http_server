import os
import urllib.parse
import main
from response import Response
import content_type
from http_state import States
import articles
from template_engine import TemplateEngine

class BaseController:

    def __init__(self):
        pass

    #GETメソッドを受け取った時
    def do_get(self, request) -> Response:
        self.path: str = urllib.parse.unquote(request.target)
        self.root, self.ext = os.path.splitext(self.path)
        self.ext = self.ext.lstrip(".")

        self.path = self.format_path(self.path)

    def format_path(self, path) -> str:
        #ディレクトリトラバーサル対策
        if (not path.find("..") == -1):
            path = "index.html"

        if (path.endswith("/")):
            path = path + "index.html"
            self.ext = "html"

            # 受け取ったpath
        if (path.startswith("/")):
            path = path.lstrip("/")

        return path
    
    def not_found(self):
        # self.path = self.path.rstrip("/") if self.path.endswith("/") else self.path
        response = Response(main.protocolVersion, States.Not_Found)
        response.body = os.path.join(main.DOCUMENT_ROOT, "not_found.html")
        self.ext = "html"

        return response


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
            self.response.body = os.path.join(main.DOCUMENT_ROOT, self.path)

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
        head, tail = os.path.split(self.path)
        if tail:
            article = articles.get_articles(tail)

            if article:
                engine = TemplateEngine(article, "template")
                self.response = Response(main.protocolVersion, States.OK)
                self.response.body = engine.render()

            else:
                self.response = self.not_found()

        else:
            self.response = Response(main.protocolVersion, States.Not_Found)
            self.response.body = os.path.join(main.DOCUMENT_ROOT, "blog.html")
            self.ext = "html"


        return self.response


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
