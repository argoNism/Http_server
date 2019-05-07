import socket
import ssl
import worker_thread
import threading

#HOST = "argonism.info"
HOST = "localhost"
HTTP = 8000
HTTPS = 443
DOCUMENT_ROOT = "/Users/usubasatsukifutoshi/Projects/SimpleWebServer/server/www"
#DOCUMENT_ROOT = "/home/argon/Http_server/www"
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
                print("443 thread started")

            except ssl.SSLError as e:
                print("ssl.SSLError", e)
                with open('errorlog.log', 'a') as f:
                    f.write(str(e))

                wraped_socket.close()
                print("socket closed")

            except ssl.SSLCertVerificationError as e:
                print("ssl.SSLCertVerificationError", e)
                with open('errorlog.log', 'a') as f:
                    f.write(str(e))

                wraped_socket.close()
                print("socket closed")
    
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
    # main()

