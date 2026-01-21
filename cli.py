import socket
import struct
def main():
    sock = socket.socket()
    sock.connect(("127.0.0.1", 1233))
    id = int(input("enter num"))
    ht_id = socket.htonl(id)
    print(ht_id)
    packed = struct.pack('I', ht_id)
    print(packed)
    sock.sendall(packed)

if __name__ == "__main__":
    main()
