#!/bin/python3
import socket
import sys
import argparse

args = sys.argv
listen = False
target = ""
port = 0

def server():
    print("[*] Starting server...")
    print(f"[*] Listening at {args[2]} port {args[3]}...")

def tryToConnect(client):
    print("[*] Connecting...")
    try:
        client.connect_ex((target, port))
        print("[*] Success!")
    except:
        if socket.error == OSError:
            print("[!] OSError: Can't connect to the address.")
        sys.exit(1)

def tryToSend(client, data):
    print("[*] Sending...")
    len_sent = client.send(data)
    if len_sent == len(data):
        print("[*] Success!")
    elif len_sent == 0:
        print("[*] Failed to send.")
    else:
        print(f"[*] Failed to send {len(data)-len_sent} bytes.")

#TODO: fix reciveData not recieving data from google

def recieveData(client):
    print("[*] Recieveing Data...")
    data = client.recv(4096)
    print(data)

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        tryToConnect(client)
        print("What will you send?")
        data = input("> ")
        tryToSend(client, data.encode('utf-8'))
        recieveData(client)

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
        
        
        

        
