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

def client():
    print("client")

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
    print(listen, target, port)
        
        
        

        
