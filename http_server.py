__author__ = "Ido Keysar"

import socket
import os
import threading
import sys
from http_functions import http_recv, http_send

web_root = r"C:\Users\1idok\PycharmProjects\taskLST\http\4.4\webroot"
def handle_client(client_soc, http_version):
    while True:
        try:
            request_line, headers, body = http_recv(client_soc)

            if not request_line:
                break

            if len(request_line.split()) < 3:
                break

            resource = request_line.split()[1]

            if request_line.startswith("POST") and resource.startswith("/upload"):
                try:
                    qury = resource.split("?")[1]
                    file_name = qury.split("file-name=")[1].split("&")[0]
                    save_path = web_root + "\\" + file_name

                    with open(save_path, "wb") as f:
                        f.write(body) # needs admin for some reason

                    print(f"saved: {file_name}")
                except Exception as e:
                    print(f"err: {e}")
                continue

            if resource.startswith("/calculate-next"):
                result_val = "5"
                if "?" in resource:
                    numEq = resource.split("?")[1]
                    if numEq.startswith("num="):
                        try:
                            num = int(numEq.split("=")[1])
                            result_val = str(num + 1)
                        except:
                            print("invalid num,")
                            result_val = "5"
                cont = result_val.encode()
                response_headers = f"Content-Type: text/html; charset=UTF-8\r\nContent-Length: {len(cont)}\r\n"
                http_send(client_soc, f"HTTP/{http_version} 200 OK\r\n", response_headers, cont)
                continue

            if resource.startswith("/calculate-area"):
                try:
                    query = resource.split("?")[1]
                    p1 = query.split("&")[0]
                    p2 = query.split("&")[1]

                    side1 = float(p1.split("=")[1])
                    side2 = float(p2.split("=")[1])

                    area = (side1 * side2) / 2
                    result = str(area)
                except:
                    result = "0.0"

                cont = result.encode()
                response_headers = f"Content-Type: text/html; charset=UTF-8\r\nContent-Length: {len(cont)}\r\n"
                http_send(client_soc, f"HTTP/{http_version} 200 OK\r\n", response_headers, cont)
                continue


            if resource == "/":
                resource = "/index.html"
            if resource == "/forbidden.html":
                http_send(client_soc, f"HTTP/{http_version} 403 Forbidden\r\n", "", b"403 Forbidden")
                continue
            elif resource == "/MovedTemporarily.html":
                response_headers = "Location: /index.html\r\n"
                http_send(client_soc, f"HTTP/{http_version} 302 Found\r\n", response_headers, b"")
                continue
            elif resource == "/internalServerError.html":
                http_send(client_soc, f"HTTP/{http_version} 500 Internal Server Error\r\n", "", b"500 Internal Server Error")
                continue

            file_path = web_root + resource

            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()

                match ext:
                    case ".html" | ".txt":
                        content_type = "text/html; charset=UTF-8"
                    case ".jpg":
                        content_type = "image/jpeg"
                    case ".js":
                        content_type = "text/javascript; charset=UTF-8"
                    case ".css":
                        content_type = "text/css"
                    case _:
                        content_type = "application/octet-stream"

                with open(file_path, "rb") as f:
                    content = f.read()

                response_headers = f"Content-Type: {content_type}\r\n"
                http_send(client_soc, f"HTTP/{http_version} 200 OK\r\n", response_headers, content)
            else:
                http_send(client_soc, f"HTTP/{http_version} 404 Not Found\r\n", "", b"404 Not Found")

            if http_version == "1.0":
                break

            if headers and headers.get('connection', '').lower() == 'close':
                print("connection close requested")
                break

        except:
            break

    client_soc.close()


def main():
    if len(sys.argv) < 2:
        print("need 1.0 or 1.1, setting 1.1")
        http_version = "1.1"
    else:
        http_version = sys.argv[1]
    if http_version != "1.0" and http_version != "1.1":
        print("use 1.0 or 1.1")
        return

    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen(10)
    print(f"Server is running on port 80 (HTTP/{http_version})...")

    while True:
        client_soc, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_soc, http_version))
        client_thread.start()


if __name__ == "__main__":
    main()