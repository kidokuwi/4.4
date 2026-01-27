import socket


def send_post_request():
    server_ip = "127.0.0.1"
    server_port = 80
    file_to_send = r"C:\Users\1idok\PycharmProjects\taskLST\http\4.4\webroot\imgs\abstract.jpg"
    file_name_on_server = r"uploaded_image.jpg"

    with open(file_to_send, "rb") as f:
        file_content = f.read()

    client_socket = socket.socket()
    client_socket.connect((server_ip, server_port))

    resource = f"/upload?file-name={file_name_on_server}"
    request_line = f"POST {resource} HTTP/1.1\r\n"
    headers = (
        f"Host: {server_ip}\r\n"
        f"Content-Length: {len(file_content)}\r\n"
        f"Content-Type: image/jpeg\r\n"
        "\r\n"
    )

    client_socket.send(request_line.encode() + headers.encode() + file_content)

    client_socket.close()


if __name__ == "__main__":
    send_post_request()