#!/bin/python3
import socket
import sys
import asyncio

bufferSize = 4096
args = sys.argv
listen = False
target = ""
port = 0

#TODO: fix bugs

def server() -> None:
    print("[*] Starting server...")
    serverSocket = socket.create_server((target, port))
    print("[*] Listening...")
    conn, addr = serverSocket.accept()
    data = b""
    with conn:
        print("[*] Connected by: ", addr)
        while True:
            data = conn.recv(bufferSize)
            if not data: break
            print(data.decode("utf-8").rstrip())

def tryToConnect() -> socket.socket:
    print("[*] Connecting...")
    try:
        clientSocket = socket.create_connection((target, port))
        clientSocket.setblocking(False)
        print("[*] Success!")
        return clientSocket
    except:
        if socket.error == OSError:
            print("[!] OSError: Can't connect to the address.")
        sys.exit(1)

async def tryToSend(client: socket.socket, data: bytes, 
                    eventLoop: asyncio.AbstractEventLoop) -> None:
    print("[*] Sending...")
    try:
        len_sent = await eventLoop.run_in_executor(None, client.send, data + b'\n')
        if len_sent == len(data) + 1:
            print("[*] Success!")
        elif len_sent == 0:
            print("[*] Failed to send.")
        else:
            print(f"[*] Failed to send {len(data)-len_sent} bytes.")
    except BrokenPipeError:
        print("[!] Lost connection.")
        exit()

async def recieveData(client: socket.socket, 
                      eventLoop: asyncio.AbstractEventLoop):
    print("[*] Recieveing Data...")
    loop = True

    while loop:
        try:
            data = await eventLoop.run_in_executor(None, client.recv, 
                                                   bufferSize)
            print(data.decode('utf-8').rstrip())
            if not data:
                print("[*] Done!")
                loop = False
            if data == b'':
                loop = False
        except BlockingIOError:
            continue

async def client() -> None:
    clientSocket: socket.socket = tryToConnect()
    eventLoop = asyncio.get_event_loop()
    while True:
        print("What will you send?")
        data = await eventLoop.run_in_executor(None, input, '> ')
        tasks = [
                tryToSend(clientSocket, data.encode('utf-8'), eventLoop),
                recieveData(clientSocket, eventLoop)
                ]
        await asyncio.gather(*tasks)

def printUsage() -> None:
    print("Usage: ./netcar [-b listen] destination port")
    print("Example: ")
    print("\t./netcar -b 0.0.0.0 9999 ")
    print("\t./netcar www.google.com 9999 ")

def parse() -> None:
    global listen
    global target
    global port

    if len(args) <= 1 or len(args) > 4:
        printUsage()
        exit()
    for i in args:
        if i == "-b":
            listen = True
            continue
        elif i.isdigit():
            port = int(i)
            continue
        else:
            target = i

if __name__ == '__main__':
    parse()
    if listen:
        server()
    else:
        asyncio.run(client())
        
        
        

        
