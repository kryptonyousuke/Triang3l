#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: MIT
#

import functools

def session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with open(".key", "r") as token_file:
                token = token_file.read().strip()
            if token == "":
                print("Error: the token can't be empty.")
                exit(1)
        except FileNotFoundError:
            print("Error: .key file does not exist.")
            exit(1)
        result = func(*args, token=token, **kwargs)
        return result
    return wrapper
