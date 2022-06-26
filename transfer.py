#!/usr/bin/env python3
import sys
import logging as log
import dataclasses
import socket
from typing import Any, Optional

HOST = '192.168.190.232'  #server.
PORT = 61345  #lspci--ubuntu            #client sends file to the server.

log.basicConfig(level=log.INFO)

"""
Helper class with static methods for sending and recieving data using sockets.
"""
class Transfer:
    @staticmethod
    def recv(conn: socket.socket):
        log.info("Blocking to read data from connection")

        while True:
            # recv() is blocking and will wait till connection is closed
            data = conn.recv(1024)
            if not data:
                break
            yield data

        log.info("Stopped recieving data from connection")

    @staticmethod
    def recv_file(conn: socket.socket, save_to: str):
        with open(save_to, "w") as f:
            for chunk in Transfer.recv(conn):
                f.write(chunk.decode())
        log.info(f"Recieved file from connection, saved to {save_to}")

    @staticmethod
    def send(conn: socket.socket, data: str):
        conn.sendall(str.encode(data))

    @staticmethod
    def send_file(conn: socket.socket, file: str):
        log.info(f"Sending file {file} to other device")
        with open(file, 'r') as f:
            Transfer.send(conn, f.read())
        log.info("Finished sending file to other device")

@dataclasses.dataclass
class ConnectedClient:
    conn: socket.socket
    addr: Any

class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen() # enable accepting connections

        self.client: Optional[ConnectedClient] = None
        log.info(f"Started server at {host}:{port}")

    """
    Block and wait for a connection from a client.
    """
    def connect(self):
        self.client = ConnectedClient(*self.socket.accept())
        log.info(f"Client from {self.client.addr} connected to server")

    """
    Disconnects from an active client, if a connection was open.
    """
    def disconnet(self):
        if self.client is None:
            return
        self.client.conn.close()
        log.info(f"Connection from client at {self.client.addr} closed")
        self.client = None

    def recv(self):
        if self.client is None:
            log.error("Tried to recieve data from unconnected client")
            return None
        yield from Transfer.recv(self.client.conn)

    def recv_file(self, save_to: str):
        if self.client is None:
            log.error("Tried to recieve data from unconnected client")
            return None
        Transfer.recv_file(self.client.conn, save_to)

    def send(self, data: str):
        if self.client is None:
            log.error("Tried to send data to unconnected client")
            return None
        Transfer.send(self.client.conn, data)

    def send_file(self, filename: str):
        if self.client is None:
            log.error("Tried to send data to unconnected client")
            return None
        Transfer.send_file(self.client.conn, filename)

    def shutdown(self):
        self.disconnet()
        self.socket.close()
        log.info("Shutdown server")


class Client:
    def __init__(self, host=HOST, port=PORT) -> None:
        self.host = host
        self.port = port

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        log.info(f"Started client and connected to server at {host}:{port}")

    def recv(self):
        yield from Transfer.recv(self.conn)

    def recv_file(self, save_to: str):
        Transfer.recv_file(self.conn, save_to)

    def send(self, data: str):
        Transfer.send(self.conn, data)

    def send_file(self, filename: str):
        Transfer.send_file(self.conn, filename)

    def shutdown(self):
        self.conn.close()
        log.info("Shutdown client")

if __name__ == "__main__":
    if sys.argv[0].startswith('python'):
        action = sys.argv[2]
    else:
        action = sys.argv[1]

    if action == 'server':
        server = Server()
        server.connect()

        file = input("Where to save file: ")
        server.recv_file(file)

        server.shutdown()
    elif action == 'client':
        client = Client()
        file = input("Filename to upload: ")

        client.send_file(file)


SERVER: Optional[Server] = None
CLIENT: Optional[Client] = None

# ----- Server Functions ------ #

def server_start():
    global SERVER
    SERVER = Server()

def server_stop():
    global SERVER
    if SERVER is None:
        return

    SERVER.shutdown()

def server_wait_for_client_to_connect():
    global SERVER
    if SERVER is None:
        return

    SERVER.connect()

def server_send_file(filepath: str):
    global SERVER
    if SERVER is None:
        return

    SERVER.send_file(filepath)

def server_recieve_file(savepath: str):
    global SERVER
    if SERVER is None:
        return

    SERVER.recv_file(savepath)

# ----- Client Functions ------ #

def client_start():
    global CLIENT
    CLIENT = Client()

def client_stop():
    global CLIENT
    if CLIENT is None:
        return

    CLIENT.shutdown()

def client_send_file(filepath: str):
    global CLIENT
    if CLIENT is None:
        return

    CLIENT.send_file(filepath)

def client_recieve_file(savepath: str):
    global CLIENT
    if CLIENT is None:
        return

    CLIENT.recv_file(savepath)

