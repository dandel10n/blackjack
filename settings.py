#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-b', '--bank', required=True, type=int)
    parser.add_argument ('-d', '--debug', action='store_true', default=False)

    return parser

parser = createParser()
cli_args = parser.parse_args(sys.argv[1:])
BANK_AMOUNT = cli_args.bank
DEBUG = cli_args.debug

if __name__ == "__main__":
    print("Это модуль, содержащий аргументы командной строки.")
    input("\nНажмите Enter, чтобы выйти.")
