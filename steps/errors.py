from ts_api import *
from behave import *
from utils import *
from requests import *

@then('I get an error {code}')
def error_step(context, code ):
    assert int(code) == context.error.response.status_code