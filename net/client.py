#!/bin/python3

"""TCP/IP client."""

import socket

client_socket = None


def init_client(host, port):
    """Initialize client and connect to server."""
    global client_socket
    client_socket = socket.socket()
    client_socket.connect((host, port))


def send_data(msg):
    """Send message to server, return result."""
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    return data


def close_client():
    """Close the client socket."""
    client_socket.close()
