#!/bin/python3

"""Main function."""

import argparse

from main import whatsapp_web as ww

parser = argparse.ArgumentParser(description="WhatsApp CLI")
parser.add_argument(
    "-v", "--visible", default=False, help="Make browser visible",
)

args = parser.parse_args()

if __name__ == "__main__":
    ww.main(args.visible)
