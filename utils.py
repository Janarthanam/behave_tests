import uuid
from requests import HTTPError

def random_str() -> str:
    return uuid.uuid4().hex

def expect_requests(func):
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
        except HTTPError as e:
            args[0].error = e
