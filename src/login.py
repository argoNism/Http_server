import socket
import ssl
import hashlib
import random, string
import articles

#HOST = "argonism.info"
HOST = "localhost"
PORT = 8950
DOCUMENT_ROOT = "/Users/usubasatsukifutoshi/Projects/SimpleWebServer/server/www"
#DOCUMENT_ROOT = "/home/argon/Http_server/www"
CRT = '/etc/letsencrypt/live/argonism.info/cert.pem'
KEY = '/etc/letsencrypt/live/argonism.info/privkey.pem'
PASSWORD = "1FOvv8BdFz0dN5nKF"

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def auth_confirm(random, password):
    hashed = hashlib.sha256(PASSWORD)
    added = hashed + random
    if added == password:
        return True
    else:
        return False

def main():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(CRT, keyfile=KEY)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print("s server listening...")

    try:

        while True:
            client_socket, client_address = server.accept()
            print("auth accepted")
            random_str = randomname(10)
            client_socket.send(random_str)

            byte_msg = client_socket.recv(1024)

            if auth_confirm(random_str, byte_msg):
                pass
    finally:
        server.close()
        # thread.stop()

if __name__ == "__main__":
    main()

