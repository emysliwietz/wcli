#!/bin/python3

"""Utility file to start server."""

from net.server import init_server
from server import server


def main(visible, port):
    init_server(port)
    server.main(visible)
