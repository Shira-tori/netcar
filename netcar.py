#!/bin/python3
import socket
import sys
import argparse

args = sys.argv

def server():
    print("[*] Starting server...")
    print(f"[*] Listening at {args[2]} port {args[3]}...")

def client():
    print("client")

if __name__ == '__main__':
    print("Usage: ./netcar [-b listen] destination port")
    print("Example: ")
    print("\t./netcar -b 0.0.0.0 9999 ")
    print("\t./netcar www.google.com 9999 ")
        
