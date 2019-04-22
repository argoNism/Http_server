from response import Response
import socket
import main
import content_type
from http_state import States
from http_state import get_states_number

SP = " "

utf8_map =[
    "text/html", "text/css", "text/plane", "text/javascript"
]

rb_map = [
    "image/png", "image/jpeg", "image/jpeg", "image/gif", "image/vnd.microsoft.icon"
]

message = ""

class ResponseMessageLine():
    def __init__(self):
        self.message = bytes()

    def add_message_line(self, msg: str) -> None:
        if(msg.__class__.__name__ == 'bytes'):
            self.message += msg + b"\n"
        else:
            self.message += msg.encode('utf-8') + b"\n"
        # self.message += msg + "\n"

def write_body_text(message_line, response, encoding: str):

    with open(response.body, encoding=encoding) as file:
        message_line.add_message_line(file.read())

def write_body_image(message_line, response, mode: str):
    with open(response.body, mode=mode) as file:
        message_line.add_message_line(file.read())


#ResponseMessageLine にstrを追加していって、最後にencodeしたやつを送る
def send_response(sock: socket, response: Response) -> None:
    response_msg = ResponseMessageLine()

    #send http resopnse status line
    response_msg.add_message_line(main.protocolVersion + SP + get_states_number(response.states) + SP + response.states.value)

    for k, v in response.headers.items():
        response_msg.add_message_line(k + ": " + v)

    response_msg.add_message_line("")

    if "Content-Type" in response.headers:
        if response.headers["Content-Type"] in utf8_map:
            write_body_text(response_msg, response, 'utf-8')
        elif response.headers["Content-Type"] in rb_map:
            write_body_image(response_msg, response, 'rb')
        else:
            write_body_image(response_msg , response, 'rb')
    else:
        write_body_text(response_msg, response, 'utf-8')

    sock.send(response_msg.message)