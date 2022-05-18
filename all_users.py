from ts_api import *
import sys

def main(host:str, user:str, password: str, groupId: str):
    session = login(host, user, password)
    #session = login_using_secret(host, user, secret, -1)
    info = session_orgs(session, host)
    switch_org(session,host=host, orgId=-1)
    #print(json.dumps(info, indent=3))

    print(get_users_in_group(session=session, host=host, groupId=groupId))


if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3], groupId=sys.argv[4])