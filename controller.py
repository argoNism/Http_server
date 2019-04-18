import os
import urllib.parse
import main
from response import Response
import content_type
from http_state import States

class Controller:

    def __init__(self):
        pass

    #GETメソッドを受け取った時
    def do_get(self, request) -> Response:
        path: str = urllib.parse.unquote(request.target)
        self.root, self.ext = os.path.splitext(path)
        self.ext = self.ext.lstrip(".")

        path = self.format_path(path)

        # make responce object so determine states code
        #指定されたuriのファイルが存在するか確認
        if os.path.exists(os.path.join(main.DOCUMENT_ROOT, path)) and os.path.isfile(os.path.join(main.DOCUMENT_ROOT, path)):
            self.response = Response(main.protocolVersion, States.OK)
            self.response.body = os.path.join(main.DOCUMENT_ROOT, path)

        #ファイルが見つからない時、not_found.htmlを送信
        else:
            path = path.rstrip("/") if path.endswith("/") else path
            self.response = Response(main.protocolVersion, States.Not_Found)
            self.response.body = os.path.join(main.DOCUMENT_ROOT, "not_found.html")
            self.ext = "html"

        self.response.add_header("Content-Type", content_type.get_content_text(self.ext))
        return self.response


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


