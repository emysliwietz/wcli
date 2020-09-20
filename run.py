#!/bin/python3

"""Main function."""

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

args = parser.parse_args()

if __name__ == "__main__":
    from main import whatsapp_web as ww

    ww.main(args.visible)
