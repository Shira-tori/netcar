#!/bin/python3
import socket
import argparse
import threading

BUFFERSIZE = 4096

class Netcar:
    def __init__(self, listen: bool, state: threading.Event, 
                 target: str, port: int, BUFFERSIZE: int):
        self.listen = listen
        self.state = state
        self.target = target
        self.port = port
        self.BUFFERSIZE = BUFFERSIZE

    def run(self):
        if self.listen == True:
            self.server()
            exit()
        self.client()

    def try_to_connect(self) -> socket.socket:
        try:
            clientSocket = socket.create_connection((target, port))
            print("[*] Connected.")
            return clientSocket
        except ConnectionRefusedError:
            print(f"[!] Could not connect to {target}:{port}. Connection Refused.")
            exit()


    def recv_data(self, clientSocket: socket.socket) -> None:
        while True:
            data = clientSocket.recv(BUFFERSIZE).decode('utf-8').rstrip()
            if not data:
                print("[!] Server disconnected.")
                break
            print(data)

    def send_data(self, clientSocket: socket.socket) -> None:
        try:
            while True:
                    data = (input() + '\n').encode('utf-8')
                    clientSocket.send(data)

                    if not state.is_set():
                        break

        except BrokenPipeError:
            print("[!] Connection closed.")
            return
            

    def client(self) -> None:
        clientSocket = self.try_to_connect()

        thread = threading.Thread(target=self.send_data, args=[clientSocket])
        thread.start()
        try:
            self.recv_data(clientSocket)
            thread.join()
        except KeyboardInterrupt:
            self.state.set()
            print("\nExiting...")
        clientSocket.close()
        exit(0)

    def handle(self, serverSocket):
        sock, _ = serverSocket.accept()
        while True:
            data = sock.recv(self.BUFFERSIZE)
            if not data:
                print("[*] Disconnected.")
                break
            print(data.decode().rstrip())

        
    def server(self) -> None:
        serverSocket = socket.create_server((self.target, self.port))
        handleThread = threading.Thread(target=self.handle, 
                                        args=[serverSocket,])
        handleThread.start()


def parse_args() -> tuple:

    parse = argparse.ArgumentParser(prog="netcat", 
                                    description="A netcat clone.") 
    parse.add_argument('target_addr')
    parse.add_argument('port', type=int)
    parse.add_argument('-b', '--bind', action='store_true')

    args = parse.parse_args()

    target = args.target_addr
    port = args.port
    listen = args.bind

    return target, port, listen

if __name__ == '__main__':
    target, port, listen = parse_args()        
    state = threading.Event()
    netcar = Netcar(listen, state, target, port, BUFFERSIZE)
    netcar.run()

