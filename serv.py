import socket
import struct

def main():
    sock = socket.socket()
    sock.bind(("0.0.0.0", 1233))
    sock.listen(20)
    cli_sock, addr = sock.accept()
    print("accepted")
    recv = cli_sock.recv(4)
    print(recv)
    unpacked, = struct.unpack("I", recv)
    print(unpacked)
    id = socket.ntohl(unpacked)
    print(id)


if __name__ == "__main__":
    main()
