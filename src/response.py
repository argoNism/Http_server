from AbstractHttpMessage import AbstractHttpMessage
from http_state import States

class Response(AbstractHttpMessage):

    def __init__(self, version: str, state: States):
        super().__init__()
        self.version: str = version
        self.states: States = state
