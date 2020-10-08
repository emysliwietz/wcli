#!/bin/python3

"""TCP/IP server."""
import socket
import time
from threading import Thread, Lock
from server.server import exec_command
from signal import signal, SIGINT

MAX_CONCURRENT_CONNECTIONS = 4
server_socket = socket.socket()
server_running = False
backend_lock = Lock()

client_list = []


def server_handle_command(cmd):
    """Handle a command in backend."""
    with backend_lock:
        data = exec_command(cmd)
    return data if data else "None"


def client_disconnect(conn):
    """Handle a client ending the connection."""
    global client_list
    for (conn_2, address, client_thread) in client_list:
        if conn == conn_2:
            client_list.remove((conn_2, address, client_thread))
            conn.close()


def client_handler(conn, address):
    """Handle commands from client."""
    conn.settimeout(1)
    while server_running:
        try:
            cmd = conn.recv(1024).decode()
            print(f"from connected user {address}: " + str(cmd))
            if cmd.lower().strip() == "quit":
                break
            data = server_handle_command(cmd)
            conn.send(data.encode())
        except:
            pass
    client_disconnect(conn)


def server_connect():
    """Wait for client to connect."""
    global client_list
    server_socket.settimeout(1)
    try:
        conn, address = server_socket.accept()
        client_thread = Thread(target=client_handler, args=(conn, address))
        client_list.append((conn, address, client_thread))
        client_thread.start()
        print("Accepted connection: " + str(address))
    except:
        pass


def server_connect_loop():
    """Continuously wait for clients to connect."""
    global server_running
    while server_running:
        if len(client_list) <= MAX_CONCURRENT_CONNECTIONS:
            server_connect()
        else:
            time.sleep(1)


connect_loop = Thread(target=server_connect_loop, args=())


def server_close():
    """Close the server connection."""
    global server_running
    server_running = False
    connect_loop.join()
    for (conn, address, client_thread) in client_list:
        client_disconnect(conn)
        client_thread.join()
    print("Closed")


def handler(signal_received, frame):
    # Handle any cleanup here
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    server_close()


def init_server(port):
    """Start the server."""
    global server_running
    server_running = True
    signal(SIGINT, handler)
    server_socket.bind(("localhost", port))
    server_socket.listen(1)
    connect_loop.start()
