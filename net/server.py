#!/bin/python3

"""TCP/IP server."""
import socket
import time
from threading import Thread

MAX_CONCURRENT_CONNECTIONS = 4
server_socket = socket.socket()
connect_loop = Thread(target=server_connect_loop, args=())
server_running = False
backend_lock = threading.Lock()

client_list = []


def server_handle_command(cmd):
    """Handle a command in backend."""
    with lock:
        data = "Handled"  # to be replaced with actual backend action
    return data


def client_disconnect(conn):
    """Handle a client ending the connection."""
    global client_list
    for (conn_2, address, client_thread) in client_list:
        if conn == conn_2:
            client_list.remove((conn_2, address, client_thread))
            conn.close()


def client_handler(conn):
    """Handle commands from client."""
    while server_running:
        cmd = conn.recv(1024).decode()
        print(f"from connected user {address}: " + str(cmd))
        if cmd.lower().strip() == "quit":
            break
        data = server_handle_command(cmd)
        conn.send(data.encode())
    client_disconnect(conn)


def server_connect():
    """Wait for client to connect."""
    global client_list
    conn, address = server_socket.accept()
    client_thread = Thread(target=client_handler, args=(conn,))
    client_list.append((conn, address, client_thread))
    client_thread.start()
    print("Accepted connection: " + str(address))


def server_connect_loop():
    """Continuously wait for clients to connect."""
    while server_running:
        if len(client_list) <= MAX_CONCURRENT_CONNECTIONS:
            server_connect()
        else:
            time.sleep(1)


def server_close():
    """Close the server connection."""
    global server_running
    server_running = False
    connect_loop.join()
    for (conn, address, client_thread) in client_list:
        client_disconnect(conn)
        client_thread.join()
    print("Closed")


def init_server(port):
    """Start the server."""
    global server_running
    server_running = True
    server_socket.bind(("localhost", port))
    server_socket.listen(1)
    connect_loop.start()
