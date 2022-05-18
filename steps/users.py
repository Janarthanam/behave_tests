from ts_api import *
from behave import *
from utils import *
from common import *

@when('Adding an user to org {org}')
def create_user_step(context, org):
    context.users = []
    user = create_user(context.session, context.config.userdata.get(
        "target"), username=random_str(), orgId=context.orgs[int(org)-1]["orgId"])
    context.users.append(user)


@when('Update {userRef} user to add orgs')
def update_user_step(context, userRef):
    user = _get_user_from_context(context, userRef)
    orgs = [int(x["orgs"]) for x in context.table]
    update_user(session=context.session, host=context.config.userdata.get(
        "target"), user=user, orgIds=orgs)


@then('{userRef} user belongs to')
def user_in_orgs(context, userRef):
    user = _get_user_from_context(context, userRef)
    orgs = [int(x["orgs"]) for x in context.table]
    user = get_user(session=context.session, host=context.config.userdata.get(
        "target"), username=user['header']['name'])
    assert orgs == user['header']['orgIds']


@then('remove {userRef} user from org {org}')
def remove_user_in_org(context, userRef, org):
    user = _get_user_from_context(context, userRef)
    delete_user(session=context.session, host=context.config.userdata.get(
        "target"), user_id=context.users[int(user)]['header']['id'], orgId=context.orgs[int(org)-1]["orgId"])


@when('I try to remove {userRef} user from group for org {org}')
def remove_user_from_group(context, userRef, org):
    user = _get_user_from_context(context, userRef)
    context.error.response = update_user(context.session, context.config.userdata.get("target"), user, groups=[context.orgs[int(org)-1]["allGroupUserId"]])
