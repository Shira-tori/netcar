#!/bin/python3
import argparse
import shlex
import socket
import subprocess
import threading

BUFFERSIZE = 4096

# fix sending keystrokes


class Netcar:


    def __init__(self, listen: bool, 
                 state: threading.Event,
                 target: str, 
                 port: int, 
                 execute: bool,
                 upload: str,
                 BUFFERSIZE: int):
        self.listen = listen
        self.state = state
        self.target = target
        self.port = port
        self.execute = execute
        self.upload = upload
        self.BUFFERSIZE = BUFFERSIZE


    def run(self):
        if self.listen == True:
            self.server()
            exit()
        self.client()


    def try_to_connect(self) -> socket.socket:
        try:
            clientSocket = socket.create_connection((self.target, self.port))
            print("[*] Connected.")
            return clientSocket
        except ConnectionRefusedError:
            print(f"[!] Could not connect to {self.target}:{self.port}. Connection Refused.")
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

                    if not self.state.is_set():
                        break

        except BrokenPipeError:
            print("[!] Connection closed.")
            return
            

    def client(self) -> None:
        clientSocket = self.try_to_connect()

        thread = threading.Thread(target=self.send_data, 
                                  args=[clientSocket])
        thread.start()
        try:
            self.recv_data(clientSocket)
            thread.join()
        except KeyboardInterrupt:
            self.state.set()
            print("\nExiting...")
        clientSocket.close()
        exit(0)

    def getData(self, sock: socket.socket):
        data = sock.recv(self.BUFFERSIZE)
        if not data:
            print("[*] Disconnected.")
            exit()

        return data

    def handle(self, serverSocket) -> None:
        sock, _ = serverSocket.accept()
        data = self.getData(sock)
        if self.execute:
            while True:
                sock.send(b'<WOW#:> ')
                result = subprocess.check_output(shlex.split(data.decode().rstrip()),
                                                 stderr=subprocess.STDOUT)
                sock.send(result)
        elif self.upload:
            with open(f'./{self.upload}', 'wb') as f:
                f.write(data)
        else:
            while True:
                print(data.decode().rstrip())

        
    def server(self) -> None:
        serverSocket = socket.create_server((self.target, self.port))
        handleThread = threading.Thread(target=self.handle, 
                                        args=[serverSocket,])
        handleThread.start()


def parse_args() -> argparse.Namespace:

    parse = argparse.ArgumentParser(prog="netcat", 
                                    description="A netcat clone.") 
    parse.add_argument('target_addr')
    parse.add_argument('port', type=int)
    parse.add_argument('-b', '--bind', action='store_true')
    parse.add_argument('-e', '--execute', action='store_true')
    parse.add_argument('-u', '--upload', action='store')

    args = parse.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()        
    state = threading.Event()
    netcar = Netcar(args.bind, state, 
                    args.target_addr, 
                    args.port, 
                    args.execute, 
                    args.upload, 
                    BUFFERSIZE)
    netcar.run()

