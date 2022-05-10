from random import random
from ts_api import *
import sys
from utils import random_str
import json

def main(host: str, user: str, password: str):
    session = login(host, user, password)
    info = session_orgs(session, host)
    print(json.dumps(info, indent=3))

    orgs = Orgs(session, host)
    org1 = orgs.create_org(name = random_str(), description= random_str())
    org2 = orgs.create_org(name = random_str(), description= random_str())
    
    user = create_user(session, host, random_str(), orgId = org1["orgId"])
    user["userContent"]["header"]["orgIds"] = org2["orgId"]

    update_user(session, host, user)

    print(json.dumps(user, indent=3))
    orgs.delete_org(org["orgId"])


if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])