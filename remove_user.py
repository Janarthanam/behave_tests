import sys
from requests import HTTPError

from ts_api import login
from ts_api import session_info
from ts_api import create_user
from utils import random_str
from ts_api import delete_user

def main(host: str, user: str, password: str) -> None:
   session = login(host = host, user=user, password=password)
   user1 = create_user(session, host=host, username=random_str() , orgId=1)
   user2 = create_user(session, host=host, username=random_str() , orgId=2)
   #login as user1
   session = login(host=host, user=user1["header"]["name"], password="Whatever123")
   try:
      delete_user(session, host=host, user_id=user2["header"]["id"])
   except HTTPError as error:
      print("Caught error:%s" % error)
   #login as admin
   session = login(host = host, user=user, password=password)
   delete_user(session, host=host, user_id=user1["header"]["id"], orgId=1)
   delete_user(session, host=host, user_id=user2["header"]["id"], orgId=2)


if __name__ == "__main__":
    main(host = sys.argv[1], user=sys.argv[2], password=sys.argv[3])


