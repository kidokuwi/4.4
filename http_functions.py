__author__ = "Ido Keysar"
import socket
def http_recv(soc):
    data_bytes = b""
    while True:
        try:
            chunk = soc.recv(1024)
            if chunk == b"":
                return None, None, None
            data_bytes += chunk
            if b"\r\n\r\n" in data_bytes:
                break
        except:
            return None, None, None
    header = data_bytes.split(b"\r\n\r\n")[0]
    body = data_bytes.split(b"\r\n\r\n",1)[1]
    header_str = header.decode()
    first_line = header_str.split("\r\n")[0]
    headers = {}
    for line in header_str.split("\r\n")[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.lower().strip()] = value.strip()
    try:
        content_length = int(headers.get("content-length"))
    except:
        content_length = 0
    while len(body) < content_length:
        chunk = soc.recv(1024)
        if chunk == b"":
            break
        body += chunk
    if content_length > 0:
        body = body[:content_length]
        return first_line, headers, body
    else:
        return first_line, headers, b""


def http_send(soc, first_line, headers, body):
    if body and len(body) > 0:
        content_length_header = f"Content-Length: {len(body)}\r\n"
        headers += content_length_header
    header_str = first_line + headers + "\r\n"
    full_response = header_str.encode() + body
    soc.sendall(full_response)

def main():
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(3)
    print("Listening on port 8001...")

    cli, addr = s.accept()
    print("New Client connected")
    request_cnt = 1

    while True:
        request, headers, body = http_recv(cli)

        if request is None:
            print("Client disconnected")
            break

        print(f"------------------------------------------ {request_cnt}")

        all_data = f"#:{request_cnt}\n----Request: {request}\n----Headers: {headers}\n----Body: {body}"
        print(all_data)


        resource = request.split()[1]

        if resource == '/':
            content = "Got Default Request<br/>" + all_data
        elif resource == "/favicon.ico":
            content = "Favicon Request:<br/>" + all_data
        else:
            content = "Else Path:<br/>" + all_data

        html = f"<html><head><title>My Site</title></head><body>{content}</body></html>"

        response_header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html.encode())}\r\n"
            "Connection: keep-alive\r\n"
            "\r\n"
        )

        response = response_header.encode() + html.encode()
        cli.send(response)

        is_http_1_0 = request.split()[2].upper() == "HTTP/1.0"
        should_close = headers.get('connection', '').lower() == 'close'

        if is_http_1_0 or should_close:
            print("Closing connection based on headers")
            break

        request_cnt += 1

    cli.close()
    s.close()


if __name__ == "__main__":
    main()