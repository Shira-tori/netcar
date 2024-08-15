#!/bin/python3
import socket
import sys
import argparse

bufferSize = 4096
args = sys.argv
listen = False
target = ""
port = 0

def server():
    print("[*] Starting server...")
    print(f"[*] Listening at {args[2]} port {args[3]}...")

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

def tryToSend(client, data):
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

#TODO: find out how to only recieve the right size of data

def recieveData(client):
    print("[*] Recieveing Data...")
    data = client.recv(bufferSize)

    while data:
        data = client.recv(bufferSize)
        print(data.decode('utf-8'))

def client():
    clientSocket = tryToConnect()
    while True:
        clientSocket.proto
        print("What will you send?")
        data = input("> ")
        tryToSend(clientSocket, data.encode('utf-8'))
        recieveData(clientSocket)

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
        
        
        

        
