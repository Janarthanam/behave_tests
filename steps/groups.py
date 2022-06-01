from steps.common import *
from ts_api import *
from utils import *
from requests import HTTPError

def _get_user_from_context(context, userRef):
    return context.users[int(userRef)] if (isinstance(userRef, int)) else context.users[-1]

@preserve_exception
@when('I add {userRef} user to an org {org} group')
def add_user_to_org_group_step(context, userRef, org):
    user = get_user_from_context(context, userRef)
    try:
        context.response = add_user_to_group(session=context.session, host=context.config.userdata.get(
            "target"), userId=user['header']['id'], group = context.orgs[int(org)-1]["allGroupUserId"])
    except HTTPError as error:
        print(error)
        context.error=error

@then('I add a group to the org {org}')
def add_group_to_org_step(context, org):
    org_id = get_relative_org_id(context, org)
    group = create_group(context.session, host=get_host(context), name=random_str(), org_id = org_id)
    get_groups(context).append(group)
    

@then("I add the user {userRef} to the group {groupRef}")
def add_user_to_group_step(context, userRef, groupRef):
    user = get_user_from_context(context, userRef)
    group = get_group_from_context(context, groupRef)
    context.response = add_user_to_group(session=context.session, host=context.config.userdata.get(
            "target"), userId=user['header']['id'], group = group['header']['id'])

