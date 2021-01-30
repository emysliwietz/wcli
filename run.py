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
    nargs=1,
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

parser.add_argument(
    "-P",
    "--profile",
    dest="profile",
    nargs=1,
    default="RussianBot",
    help="Override profile (default: RussianBot)",
)

args = parser.parse_args()

if __name__ == "__main__":
    with suppress(TypeError):
        args.port = int(args.port[0])

    with suppress(TypeError):
        args.server = args.server[0]
    if args.server == False:
        args.server = "localhost"

    if args.server == True:
        from main.server import main

        main(args.visible, args.port, args.profile)
    else:
        print(args.server)
        from main.client import main

        main(args.server, args.port)
