from types import LambdaType
from ts_api import *
from behave import *
from utils import *
from requests import *

@then('I get an error {code}')
def error_step(context, code ):
    assert int(code) == context.error.response.status_code

@then('I get a status {code}')
def response(context, code):
    assert int(code) == context.response.status_code

@then('I get response "{attribute}" value is "{value}"')
def response_map_contain(context, attribute: str, value):
    assert(context.response[attribute] == value)