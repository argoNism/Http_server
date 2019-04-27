from request import Request
import re

#　各parse_***関数は、Requestを受け取って、それのフィールドメンバに代入して、そのRequestを返す。

header = "(.+)\:\s(.+)"

def parse_requestline(msg: str, request: Request) -> Request:
    params = msg.split(" ")

    request.type, request.target, request.version = (params[0], params[1], params[2])

    return request


def parse_header(lines, request) -> Request:
    for line in lines:
        print(line)
        result = re.search(header, line)
        print(result)

        if result is not None:
            print(result.group(1), result.group(2))
            request.add_header(result.group(1), result.group(2))

        if line == "\n":
            break

    return request


def parse_body(msg, request):
    pass

#
def parse_request(msg: str):
    print("^^^^^^ parse_request ^^^^^^")

    request: Request = Request()

    #ジェネレーターオブジェクトの生成
    lines = coroutine(msg)

    #リクエストラインを抽出
    request_line = next(lines)
    print("request-line:", request_line)

    #
    if request_line is None:
        return None

    request_header = next(lines)
    print("request-headers:", request_header)

    request_body = next(lines)
    print("request-body:", request_body)

    request = parse_requestline(request_line, request)

    request = parse_header(request_header, request)

    return request


def coroutine(msg: str):
    lines = msg.splitlines()
    if lines:
        yield lines[0]
    else:
        yield None

    headers = []
    body = []
    body_linenum = 0
    for i, line in enumerate(lines[1:]):
        if line == "\n":
            body_linenum = i
            break
        headers.append(line)
    yield headers

    for i, line in enumerate(lines[body_linenum:]):
        body.append(line)

    yield  body