import socket
import ssl
import worker_thread
import threading

HOST = "118.27.0.160"
#HOST = "localhost"
HTTP = 80
HTTPS = 443
#DOCUMENT_ROOT = "/Users/usubasatsukifutoshi/Projects/SimpleWebServer/server/www"
DOCUMENT_ROOT = "/home/argon/server/www"
CRT = '/etc/letsencrypt/live/argonism.info/cert.pem'
KEY = '/etc/letsencrypt/live/argonism.info/privkey.pem'
protocolVersion = "HTTP/1.1"

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
                # thread = worker_thread.WorkerThread(wraped_socket)
                # thread.start()
                print("443 thread started")

            except ssl.SSLError as e:
                print("ssl.SSLError: " + str(e))

                with open("errorlog.txt", "w") as file:
                    file.write(str(e)

        #デバック用。一回リクエストを受け取って終わる
        # while True:
        #     try:
        #         server = ctx.wrap_socket(server);
        #         client_socket, client_address = server.accept()
        #         print("accepted")
        #         thread = worker_thread.WorkerThread(client_socket)
        #         thread.start()
        #         print("started thead")
        #     finally:
        #         break

    finally:
        server.close()
        # thread.stop()


def receive_http():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, HTTP))
    server.listen(1)
    print("p server listening...")

    try:

        while True:
            client_socket, client_address = server.accept()
            print("80 accepted")
            common(client_socket, client_address)
            # thread = worker_thread.WorkerThread(client_socket)
            # thread.start()
            print("80 thread started")

            #デバック用。一回リクエストを受け取って終わる
            # while True:
            #     try:
            #         server = ctx.wrap_socket(server);
            #         client_socket, client_address = server.accept()
            #         print("accepted")
            #         thread = worker_thread.WorkerThread(client_socket)
            #         thread.start()
            #         print("started thead")
            #     finally:
            #         break

    finally:
        server.close()
        # thread.stop()

if __name__ == "__main__":
    http = threading.Thread(target=receive_http)
    http.start()
    main()

