from random import random
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

    #create orgs
    orgs = Orgs(session, host)
    org1 = orgs.create_org(name = random_str(), description= random_str())
    org2 = orgs.create_org(name = random_str(), description= random_str())
    print(f"created org: {org1['orgId']}")
    print(f"created org: {org2['orgId']}")

    #currently we can't add users to multiple orgs, so update
    mix_org_user = create_user(session, host=host, username=random_str(), orgId=org1["orgId"])
    print(f"User mix_org_user {mix_org_user['header']['name']} created in orgs {mix_org_user['header']['orgIds']} by {mix_org_user['header']['author']} modified by {mix_org_user['header']['modifiedBy']}")
    update_user(session, host, mix_org_user ,orgIds = [org1["orgId"],org2["orgId"]])

    groups = list_user_group(session, host=host, userId= mix_org_user["header"]["id"])
    print(groups)

    retrieved_user = get_user(session, host, username = mix_org_user["header"]["name"])
    print(f"User mix_org_user {retrieved_user['header']['name']} updated to orgs {retrieved_user['header']['orgIds']} by {retrieved_user['header']['author']} modified by {retrieved_user['header']['modifiedBy']}")


    #create org admin
    org_admin = create_user(session, host=host, username=random_str(), orgId=org1["orgId"])
    print(f"User org_admin {org_admin['header']['name']} created in orgs {org_admin['header']['orgIds']} by {org_admin['header']['author']} modified by {org_admin['header']['modifiedBy']}")
    add_user_to_group(session,host=host, userId = org_admin['header']['id'], group = org1["defaultAdminUserGroupId"])
    print(f"User org_admin {org_admin['header']['name']} in groups {list_user_group(session, host=host, userId=org_admin['header']['id'])}")

    #login as org admin and create org user   
    session = login(host, org_admin["header"]["name"], "Whatever123!@")
    session_info = session_orgs(session,host)
    print(f"User org_admin {org_admin['header']['name']} is logged in org {session_info['currentOrgId']}")
    test_user = create_user(session, host, random_str())
    print(f"User org1_user {test_user['header']['name']} created in orgs {test_user['header']['orgIds']} by {test_user['header']['author']} modified by {test_user['header']['modifiedBy']}")
    

    #as an org admin change mix org user by adding him to admin group
    add_user_to_group(session,host=host, userId = mix_org_user['header']['id'], group = org1["defaultAdminUserGroupId"])
    print(f"User mix_org_user {mix_org_user['header']['name']} in groups {list_user_group(session, host=host, userId=mix_org_user['header']['id'])}")
    retrieved_user = get_user(session, host, username = mix_org_user["header"]["name"])
    print(f"User mix_org_user {retrieved_user['header']['name']} updated to orgs {retrieved_user['header']['orgIds']} by {retrieved_user['header']['author']} modified by {retrieved_user['header']['modifiedBy']}")
    

    #login as tenant admin with -1
    session = login(host, user, password)
    switch_org(session,host=host, orgId=-1)

    #check on mix_org_user
    print(f"User mix_org_user {mix_org_user['header']['name']} in groups {list_user_group(session, host=host, userId=mix_org_user['header']['id'])}")

    #remove user from org1 and make him org2 user
    update_user(session, host, org_admin ,orgIds = [org2["orgId"]])
    org_admin_updated = get_user(session, host, username = org_admin["header"]["name"])
    print(f"User org1_admin {org_admin_updated['header']['name']} updated to orgs {org_admin_updated['header']['orgIds']}")

    #now suddenly test_user in org1 no longer has old org admin association
    retrieved_user = get_user(session, host, username = test_user["header"]["name"])
    print(f"User org1_user {retrieved_user['header']['name']} updated to orgs {retrieved_user['header']['orgIds']} by {retrieved_user['header']['author']} modified by {retrieved_user['header']['modifiedBy']}")
    
    #check on our org admin
    print(f"User org1_admin {org_admin['header']['name']} in groups {list_user_group(session, host=host, userId=org_admin['header']['id'])}")

def login_using_secret(host: str, user: str, secret: str, orgId: int = -1):
    token = get_auth_token(host=host, user=user, secret_key=secret, orgId=orgId)
    return login_as_user(host=host, user=user, token=token, redirect_host=host)

if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])
