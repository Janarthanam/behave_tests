from ts_api import *
from utils import *
from requests import HTTPError

def _get_user_from_context(context, userRef):
    return context.users[int(userRef)] if (isinstance(userRef, int)) else context.users[-1]

@expect_requests
@when('I add {userRef} user to an org {org} group')
def add_user_to_group_step(context, userRef, org):
    user = _get_user_from_context(context, userRef)
    try:
        context.response = add_user_to_group(session=context.session, host=context.config.userdata.get(
            "target"), userId=user['header']['id'], group = context.orgs[int(org)-1]["allGroupUserId"])
    except HTTPError as error:
        print(error)
        context.error=error