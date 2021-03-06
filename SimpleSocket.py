import socket
import pygame, sys
import time
    
class SimpleSocket:
    """ 
      - Very simple Socket connection class
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def close(self):
        self.sock.close()

    def sendMessage(self, msg):

        sent = self.sock.sendall(msg[:].encode())
        if sent == 0:
            raise RuntimeError("socket connection broken")


    def receiveMessage(self):
            try:
                msg = self.sock.recv(1024)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    return ""
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:
                msg = msg.decode("utf-8")
                return msg

