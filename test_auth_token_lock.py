import sys
from time import sleep
from requests.exceptions import HTTPError

from ts_api import get_auth_token
from ts_api import login_as_user
from ts_api import session_info

def main(host: str, user: str, secret_key: str) -> None:
    token = get_auth_token(host, user, secret_key)
    session = login_as_user(host, user, token, host)
    session_info_d = session_info(session, host)
    sleep(5 * 60)

    print("Attempting expired login..")
    for i in range(10):
        try:
            login_as_user(host, user, token, host)
        except HTTPError as error:
            print("Caught error:%s" % error)
    
    print("Attempting good login after expired login...")
    token = get_auth_token(host, user, secret_key)
    session = login_as_user(host, user, token, host)
    session_info_d = session_info(session, host)

    print("Attempting bad login..")
    for i in range(10):
        try:
            login_as_user(host, user, token + "bad", host)
        except HTTPError as error:
            print("Caught error:%s" % error)

    print("Attempting good login after expired login...")
    token = get_auth_token(host, user, secret_key)
    session = login_as_user(host, user, token, host)
    session_info_d = session_info(session, host)

if __name__ == "__main__":
    main(host = sys.argv[1], user = sys.argv[2], secret_key = sys.argv[3])


