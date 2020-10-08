#!/bin/python3

"""Main function."""

from contextlib import suppress
import argparse

parser = argparse.ArgumentParser(description="WhatsApp CLI")
parser.add_argument(
    "-v",
    "--visible",
    dest="visible",
    action="store_true",
    default=False,
    help="Make browser visible",
)

parser.add_argument(
    "-s",
    "--server",
    dest="server",
    action="store_true",
    default=False,
    help="Start in server mode",
)

parser.add_argument(
    "-c",
    "--client",
    dest="server",
    action="store_false",
    default=True,
    help="Start in client mode (default)",
)

parser.add_argument(
    "-p",
    "--port",
    dest="port",
    nargs=1,
    default=5665,
    help="Override port (default 5665)",
)

args = parser.parse_args()

if __name__ == "__main__":
    with suppress(TypeError):
        args.port = int(args.port[0])

    if args.server:
        print("Server")
        from main.server import main

        main(args.visible, args.port)
    else:
        print("Client")
