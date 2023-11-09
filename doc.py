from ts_api import login
from ts_api import get_api_doc
import sys

def main(host: str):
    session = login(host=host, user="tsadmin", password="admin")
    print(get_api_doc(host = host, session=session))

if __name__ == "__main__":
    main(host = sys.argv[1])