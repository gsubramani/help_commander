import socket
import sys


MY_IP_ADDRESS = '10.0.0.53'
BOARD_01_IP_ADDRESS = '10.0.0.45'

localPort = 80

# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = (BOARD_01_IP_ADDRESS, localPort)

# sock.connect(server_address)

# sock.bind()

# try:
#     sock.send(bytes('Hello World\n', encoding='ascii'))
# finally: 
#     sock.close()

MSGLEN = 10

class MySocket:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

soc = MySocket()


soc.connect(BOARD_01_IP_ADDRESS, localPort)

soc.mysend(bytes('Hello World\n', encoding='ascii'))