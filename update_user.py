from random import random
from sqlite3 import SQLITE_CREATE_TEMP_TABLE
from ts_api import *
import sys
from utils import random_str
import json

def main(host: str, user: str, password: str=None, secret: str = None):
    #session = login(host, user, password)
    session = login_using_secret(host, user, secret, -1)
    info = session_orgs(session, host)
    #print(json.dumps(info, indent=3))

    orgs = Orgs(session, host)
    org1 = orgs.create_org(name = random_str(), description= random_str())
    org2 = orgs.create_org(name = random_str(), description= random_str())
    print(org1)
    print(org2)

    user = create_user(session, host, random_str(), orgId = org1["orgId"])
    print(json.dumps(user, indent=4))

    update_user(session, host, user,orgIds = [org2["orgId"]])
    retrieved_user = get_user(session, host, username = user["header"]["name"])
    print(retrieved_user["header"]["orgIds"])

    #orgs.delete_org(org1["orgId"])
    #orgs.delete_org(org2["orgId"])
    

def login_using_secret(host: str, user: str, secret: str, orgId: int = -1):
    token = get_auth_token(host=host, user=user, secret_key=secret, orgId=orgId)
    return login_as_user(host=host, user=user, token=token, redirect_host=host)

if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], secret=sys.argv[3])
