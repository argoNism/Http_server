from request import Request
import re
import urllib.parse

#　各parse_***関数は、Requestを受け取って、それのフィールドメンバに代入して、そのRequestを返す。

def parse_requestline(msg: str, request: Request) -> Request:
    params = msg.split(" ")

    request.type, request.target, request.version = (params[0], params[1], params[2])

    print("target:", params[1])
    return request


def parse_header(lines, request) -> Request:
    for line in lines:
        result = re.search("(.+)\:\s(.+)", line)

        if result is not None:
            request.add_header(result.group(1), result.group(2))

        if line == "\n":
            break

    return request


def parse_body(msg, request):
    body_list = msg.split("&")
    print("body_list", body_list)
    if body_list:
        lines = {}
        for line in body_list:
            key_value = line.split("=")
            print("key_value", key_value)
            if key_value:
                break
            lines[key_value[0]] = urllib.parse.unquote(key_value[1])

        request.body = lines

    return request

#  最初に呼び出されるメソッド
def parse_request(msg: str):
    print("^^^^^^ parse_request ^^^^^^")

    request: Request = Request()

    #ジェネレーターオブジェクトの生成
    lines = coroutine(msg)

    #リクエストラインを抽出
    request_line = next(lines)

    #
    if request_line is None:
        return None

    request_header = next(lines)

    request_body = next(lines)
    print("request-body:", request_body)

    request = parse_requestline(request_line, request)

    request = parse_header(request_header, request)

    request = parse_body(request_body, request)

    return request


def coroutine(msg: str):
    # まずリクエストを各行に刻む
    lines = msg.splitlines()

    # リクエストラインの取得
    if lines:
        yield lines[0]
    else:
        yield None

    # ヘッダー部分の取得
    headers = []
    body_linenum = 0
    for i in range(1, len(lines)):
        if lines[i] == '':
            body_linenum = i + 1
            yield headers

        headers.append(lines[i])

    # ボディの取得
    body = ""
    for line in lines[body_linenum:]:
        body += line

    yield  body