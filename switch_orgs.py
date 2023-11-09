
import sys
import json
from ts_api import *

def main(host: str, user: str, password: str):
    session = login(host=host, user=user, password=password)
    
    info = session_info(session, host=host)
    print(f"user logged in session {info['currentOrgId']}")

    #info = session_orgs(session, host=host)
    #print(f"user logged in session {info["currentOrgId"]}")

    response = session_orgs(session, host)
    print(response)

    switch_org(session, host=host, orgId=0)

    #info = session_orgs(session, host=host)
    #print(f"user logged in session {info["currentOrgId"]}")
    info = session_info(session, host=host)
    print(f"user logged in session {info['currentOrgId']}")


if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])
