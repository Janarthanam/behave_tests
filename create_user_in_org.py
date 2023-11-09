from ts_api import *
import sys
from utils import random_str
import json

def main(host: str, user: str, password: str=None, secret: str = None):
    session = login(host, user, password)
    switch_org(session, host=host, orgId=-1)
    #print(json.dumps(info, indent=3))

    orgs = Orgs(session, host)
    org1 = orgs.create_org(name = random_str(), description= random_str())
    print(org1)

    #switch_org(session=session, host=host, orgId=org1["orgId"])
    user = create_user(session, host, random_str())
    print(json.dumps(user, indent=4))

    #orgs.delete_org(org1["orgId"])
    #orgs.delete_org(org2["orgId"])
    

def login_using_secret(host: str, user: str, secret: str, orgId: int = -1):
    token = get_auth_token(host=host, user=user, secret_key=secret, orgId=orgId)
    return login_as_user(host=host, user=user, token=token, redirect_host=host)

if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])
