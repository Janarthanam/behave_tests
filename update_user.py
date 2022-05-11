from random import random
from sqlite3 import SQLITE_CREATE_TEMP_TABLE
from ts_api import *
import sys
from utils import random_str
import json

def main(host: str, user: str, password: str=None, secret: str = None):
    session = login(host, user, password)
    #session = login_using_secret(host, user, secret, -1)
    info = session_orgs(session, host)
    switch_org(session,host=host, orgId=-1)
    #print(json.dumps(info, indent=3))

    orgs = Orgs(session, host)
    org1 = orgs.create_org(name = random_str(), description= random_str())
    org2 = orgs.create_org(name = random_str(), description= random_str())
    print(f"created org: {org1['orgId']}")
    print(f"created org: {org2['orgId']}")

    user = create_user(session, host, random_str(), orgId = org1["orgId"])
    print(f"User created in orgs {user['header']['orgIds']}")

    update_user(session, host, user,orgIds = [org2["orgId"]])
    retrieved_user = get_user(session, host, username = user["header"]["name"])
    print(f"User updated to orgs {retrieved_user['header']['orgIds']}")

    #orgs.delete_org(org1["orgId"])
    #orgs.delete_org(org2["orgId"])
    

def login_using_secret(host: str, user: str, secret: str, orgId: int = -1):
    token = get_auth_token(host=host, user=user, secret_key=secret, orgId=orgId)
    return login_as_user(host=host, user=user, token=token, redirect_host=host)

if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])
