import socket

host = "localhost" 
port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))

with open("request.txt") as file:
    msg: str = file.read()
    client.send(msg.encode('utf-8'))

# 新しいバイト配列を返す。
data = bytes()
msg = ''
# ソケットから4096バイトを繰り返し読み込み、デリミタが表示されるまでバイトをデータに格納する
while not msg:
    # ソケットからデータを受信し、結果を bytes オブジェクトで返します。一度に受信するデータは、4096bufsize
    recvd = client.recv(1024)
    print(recvd)
    if len(recvd) == 0:
        break
        # ソケットが途中で閉じられたら
        # raise ConnectionError()
    data = data + recvd

with open("response.txt", mode='w') as file:
    file.write(data.decode("utf-8"))