import AbstractHttpMessage

class Request(AbstractHttpMessage.AbstractHttpMessage):
    def __init__(self):
        super(Request, self).__init__()
        self.type: str = ""
        self.target: str = ""
        self.version: str = ""

    def get_method(self):
        return self.meth
