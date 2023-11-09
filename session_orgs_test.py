import sys
import json
from textwrap import indent
from ts_api import login
from ts_api import session_org_info

def check_session_orgs(host: str, user: str, password: str):
    session = login(host, user, password)
    print(json.dumps(session_org_info(session, host), indent = 3))

if __name__ == "__main__":
    check_session_orgs(host = sys.argv[1], user = sys.argv[2], password = sys.argv[3]) 