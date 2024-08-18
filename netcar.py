#!/bin/python3
import socket
import argparse
import threading

BUFFERSIZE = 4096
listen = False
state = threading.Event()
target = ""
port = 0

def try_to_connect() -> socket.socket:
    try:
        clientSocket = socket.create_connection((target, port))
        print("[*] Connected.")
        return clientSocket
    except ConnectionRefusedError:
        print(f"[!] Could not connect to {target}:{port}. Connection Refused.")
        exit()


def recv_data(clientSocket: socket.socket) -> None:
    while True:
        data = clientSocket.recv(BUFFERSIZE).decode('utf-8').rstrip()
        print(data)
        if not data:
            print("[!] Server disconnected.")
            break

def send_data(clientSocket: socket.socket) -> None:
    try:
        while True:
                data = (input() + '\n').encode('utf-8')
                clientSocket.send(data)

                if not state.is_set():
                    break

    except BrokenPipeError:
        print("[!] Connection closed.")
        return
        

def client() -> None:
    global state
    clientSocket = try_to_connect()

    thread = threading.Thread(target=send_data, args=[clientSocket])
    thread.start()
    try:
        recv_data(clientSocket)
        thread.join()
    except KeyboardInterrupt:
        state.set()
        print("Exiting...")
    clientSocket.close()
    exit(0)
    
    

def server() -> None:
    pass

def parse_args() -> None:
    global target
    global port
    global listen

    parse = argparse.ArgumentParser(prog="netcat", 
                                    description="A netcat clone.") 
    parse.add_argument('target_addr')
    parse.add_argument('port', type=int)
    parse.add_argument('-b', '--bind', action='store_true')

    args = parse.parse_args()

    target = args.target_addr
    port = args.port
    listen = args.bind

if __name__ == '__main__':
    parse_args()        
    if listen:
        server()
        exit(0)
    client()

