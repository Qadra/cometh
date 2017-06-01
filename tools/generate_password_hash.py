#! /usr/bin/env python3

from getpass import getpass
from crypt import crypt, mksalt, METHOD_SHA512

if __name__ == "__main__":
    pwd = getpass("Input password to be hashed: ")
    h = crypt(pwd, mksalt(METHOD_SHA512))

    print(h)
