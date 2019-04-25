import threading
import parse
from request import Request
from response import Response
from controller import NormalController
import route
import logger
import send_response

class WorkerThread(threading.Thread):
    def __init__(self, s, ip):
        super(WorkerThread, self).__init__()
        self.sock = s
        self.client_address = ip

    def run(self):
        print("run started")
        
        sum_msg = ""
        byte_msg = self.sock.recv(1024)

        sum_msg += byte_msg.decode('utf-8')
        print("request:", sum_msg)
        print("request length:", len(sum_msg))

        response: Response = self.handle_request(sum_msg)

        if response:
            send_response.send_response(self.sock,response)
        else:
            pass

        self.sock.close()


    def handle_request(self, msg) -> Response:
        # recieve all data from client

        request: Request = parse.parse_request(msg)
        if not request:
            return None
        logger.Logger.add_row(msg, self.client_address, request)

        controller: NormalController = route.route(request)
        response: Response = controller.do_get(request)

        return response

