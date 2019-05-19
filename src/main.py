import socket
import ssl
import worker_thread
import threading
import sys, traceback
import smtplib
from email.mime.text import MIMEText
from twitter import *
from config import *

# HOST = "localhost"
# DOCUMENT_ROOT = "/Users/usubasatsukifutoshi/Projects/SimpleWebServer/server/www"
# HTTP = 8000
HOST = "argonism.info"
HTTP = 80
HTTPS = 443
DOCUMENT_ROOT = "/home/argon/Http_server/www"
CRT = '/etc/letsencrypt/live/argonism.info/cert.pem'
KEY = '/etc/letsencrypt/live/argonism.info/privkey.pem'
protocolVersion = "HTTP/1.1"

t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET_KEY))


def send_dm(msg):
    t.direct_messages.events.new(
    _json={
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": t.users.show(screen_name="argo_nism")["id"]},
                "message_data": {
                    "text": msg}}}})

def common(sock, ip):
    thread = worker_thread.WorkerThread(sock, ip)
    thread.start()

def main():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(CRT, keyfile=KEY)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, HTTPS))
    server.listen(1)
    print("s server listening...")

    try:

        while True:
            client_socket, client_address = server.accept()
            print("443 accepted")
            try:
                wraped_socket = ctx.wrap_socket(client_socket, server_side=True)
                print("socket wrapped")
                common(wraped_socket, client_address)
                print("443 thread started")

            except ssl.SSLError as e:
                print("ssl.SSLError", e)
                with open('errorlog.log', 'a') as f:
                    f.write(str(e))

                # wraped_socket.close()
                # print("socket closed")

            except ssl.CertificateError as e:
                print("ssl.CertificateError", e)
                with open('errorlog.log', 'a') as f:
                    f.write(str(e))

            except:
                main_txt = traceback.format_exc()
                send_dm("Http server exception occurred!!\n" + main_txt)
                # wraped_socket.close()
                # print("socket closed")
    
    finally:
        server.close()
        # thread.stop()


def receive_http():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, HTTP))
    server.listen(1)
    print("p server listening...")

    try:

        # while True:
        #     client_socket, client_address = server.accept()
        #     print("80 accepted")
        #     common(client_socket, client_address)
        #     print("80 thread started")

        client_socket, client_address = server.accept()
        print("80 accepted")
        common(client_socket, client_address)
        print("80 thread started")

    finally:
        server.close()
        # thread.stop()

if __name__ == "__main__":
    http = threading.Thread(target=receive_http)
    http.start()
    main()

