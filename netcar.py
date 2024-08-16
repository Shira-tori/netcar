#!/bin/python3
import socket
import sys
import threading

bufferSize = 4096
args = sys.argv
listen = False
target = ""
port = 0

#TODO: fix having to press ctrl-c twice to quit

def server():
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

def tryToConnect():
    print("[*] Connecting...")
    try:
        clientSocket = socket.create_connection((target, port))
        print("[*] Success!")
        return clientSocket
    except:
        if socket.error == OSError:
            print("[!] OSError: Can't connect to the address.")
        sys.exit(1)

def tryToSend(client):
    print("What will you send?")
    data = input("> ")
    data = data.encode('utf-8')
    print("[*] Sending...")
    try:
        len_sent = client.send(data + b'\n')
        if len_sent == len(data) + 1:
            print("[*] Success!")
        elif len_sent == 0:
            print("[*] Failed to send.")
        else:
            print(f"[*] Failed to send {len(data)-len_sent} bytes.")
    except BrokenPipeError:
        print("[!] Lost connection.")
        exit()
    except KeyboardInterrupt:
        exit()

def recieveData(client):
    loop = True

    while loop:
        data = client.recv(bufferSize)
        print('\n[*] Recieved data: ', data.decode('utf-8').rstrip(), 
              '\n> ', end='')

        if not data:
            loop = False

def client():
    clientSocket = tryToConnect()
    while True:
        threading.Thread(target=recieveData, 
                         args=[clientSocket]).start()
        tryToSend(clientSocket)

def printUsage():
    print("Usage: ./netcar [-b listen] destination port")
    print("Example: ")
    print("\t./netcar -b 0.0.0.0 9999 ")
    print("\t./netcar www.google.com 9999 ")

def parse():
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
        client()
        
        
        

        
