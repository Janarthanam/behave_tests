import uuid
from requests import *
import requests

def random_str() -> str:
    return uuid.uuid4().hex

def log_raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(response.request.body)
        print(response.text)
        raise e

def preserve_exception(func):
    def wrapper(context, *args, **kwargs):
        try:
            resp = func(context, *args, **kwargs)
        except HTTPError as e:
            context.error = e
    return wrapper
