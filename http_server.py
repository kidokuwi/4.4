__author__ = "Ido Keysar"

import socket
import os
import threading
import sys
from http_functions import http_recv, http_send


def handle_client(client_soc, http_version):
    while True:
        try:
            request_line, headers, _ = http_recv(client_soc)

            if not request_line:
                break

            if not request_line.startswith("GET") or len(request_line.split()) < 3:
                break

            resource = request_line.split()[1]
            if resource == "/":
                resource = "/index.html"

            file_path = resource.lstrip("/")

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