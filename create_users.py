#!/usr/bin/env python3
import sys
import os
from ts_api import create_user
from ts_api import login

def main(host: str, user: str, count: int):
    session = login(host, 'tsadmin', 'admin')
    for i in range(0, count):
        print(create_user(session, host, f"{user}{i}"))

if __name__ == "__main__":
    main(host = sys.argv[1], user = sys.argv[2], count = int(sys.argv[3]))
