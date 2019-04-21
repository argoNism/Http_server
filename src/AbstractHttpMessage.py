
### coding: UTF-8
class AbstractHttpMessage:

    def __init__(self):
        #httpメッセージのヘッダーを、名前と値で格納する変数
        self.headers: dict = {}
        self.body: str = ""

    def add_header(self, name, value):
        self.headers[name] = value

    # def set_body(self, body):
    #     self.body = body
