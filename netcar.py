#!/bin/python3
import socket
import sys

args = sys.argv

def server():
    print("[*] Starting server...")
    print(f"[*] Listening at {args[2]} port {args[3]}...")

def client():
    print("client")

if __name__ == '__main__':
    if len(args) == 4:
        server()
    elif len(args) == 3:
        client()
    else:
        print("Usage: ./netcar [-b listen] destination port")
        print("Example: ")
        print("\t./netcar -b 0.0.0.0 9999 ")
        print("\t./netcar www.google.com 9999 ")
        
