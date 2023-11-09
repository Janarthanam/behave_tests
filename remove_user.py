import sys
from requests import HTTPError

from ts_api import *
from utils import *

def main(host: str, user: str, password: str) -> None:
   session = login(host = host, user=user, password=password)

   orgs = Orgs(session, host)
   org1 = orgs.create_org(name = random_str(), description= random_str())
   org2 = orgs.create_org(name = random_str(), description= random_str())

   
   user1 = create_user(session, host=host, username=random_str() , orgId=1)
   org_admin1 = create_user(session, host=host, username=random_str() , orgId=1)

   switch_org(session, host=host, orgId=org2['orgId'])

   try:
      delete_user(session, host=host, user_id=user1["header"]["id"])
   except HTTPError as error:
      print("Caught error:%s" % error)
   
   #login as admin

   session = login(host = host, user=org_admin1["header"]["name"], password="Whatever123")
   try:
      delete_user(session, host=host, user_id=user1["header"]["id"])
   except HTTPError as error:
      print("Caught error:%s" % error)   
      
   #delete_user(session, host=host, user_id=user1["header"]["id"], orgId=1)
   #delete_user(session, host=host, user_id=user2["header"]["id"], orgId=2)


if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])


