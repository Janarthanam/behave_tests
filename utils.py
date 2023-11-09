import uuid
from requests import *
import requests

def random_str() -> str:
    return uuid.uuid4().hex


def request_wrapper(fn: lambda) -> lambda:
    #check response
    try:
        return =


import inspect
def wrap_behave(api: module):
    for name, fn in inspect.getmembers(api, inspect.isfunction):
        setattr(api, name, ts_api_wrapper(fn))

def log_raise_for_status(response: requests.Response):
    try:
        response.raise_for_status()
    except HTTPError as e:
        print(response.request.body)
        print(response.text)
        raise e

def behave_wrapper_for_api(func: lambda):
    def wrapper(context, *args, **kwargs):
        try:
            resp = func(context, *args, **kwargs)
        except HTTPError as e:
            context.error = e
    return wrapper
