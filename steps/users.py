from ts_api import *
from behave import *
from utils import *
from common import *
import sys

@when('Adding an user to the org {org} and group {groupRef}')
@when('Adding an user to org {org}')
@when('I add an user')
def create_user_step(context, org=None, groupRef=None):
    groups=None
    if not groupRef is None:
        groups = [get_group_from_context(context, groupRef)['header']['id']]
    user = create_user(context.session, context.config.userdata.get(
        "target"), username=random_str(), orgId=get_relative_org_id(context, org), groups=groups)
    get_users(context).append(user)
    #print(user)

@when("I get the user {userRef}")
def get_the_user(context, userRef):
    user = get_user_from_context(context, userRef)
    user = get_user(session=context.session, host=context.config.userdata.get(
        "target"), username=user['header']['name'])
    print(f"get user {user}")
    update_user_in_context(context, userRef, user)

@when('Update {userRef} user to modify orgs')
@when('I update the user {userRef}')
@when('I update the user {userRef} to add group {groupRef}')
def update_user_step(context, userRef, groupRef=None):
   
    #get before update 
    get_the_user(context, userRef)
    user = get_user_from_context(context, userRef)

    orgs = None
    if (not context.table is None) and ("orgs" in context.table.headings):
        orgs = [get_relative_org_id(context, int(x["orgs"])) for x in context.table]

    groups = []
    if groupRef:
        print(get_group_from_context(context,groupRef))
        group_id = get_group_from_context(context, groupRef)['header']['id']
        groups.append(group_id)
        
    update_user(session=context.session, host=context.config.userdata.get(
        "target"), user=user, orgIds=orgs, groups=groups)


@then('{userRef} user belongs to')
def user_in_orgs(context, userRef):
    user = get_user_from_context(context, userRef)
    user = get_user(session=context.session, host=context.config.userdata.get(
        "target"), username=user['header']['name'])
    orgs = [get_relative_org_id(context, int(x["orgs"])) for x in context.table]
    assert orgs == user['header']['orgIds']


@then('remove {userRef} user from org {org}')
def remove_user_in_org(context, userRef, org):
    user = get_user_from_context(context, userRef)
    delete_user(session=context.session, host=context.config.userdata.get(
        "target"), user_id=user['header']['id'], orgId=context.orgs[int(org)-1]["orgId"])


@when('I try to remove {userRef} user from group for org {org}')
def remove_user_from_group(context, userRef, org):
    user = get_user_from_context(context, userRef)
    try:
        update_user(context.session, context.config.userdata.get("target"), user, groups=[context.orgs[int(org)-1]["allGroupUserId"]])
    except HTTPError as e:
        context.error = e

@Then('{userRef} user belongs to group')
def user_belongs_to_group(context, userRef):
    user = get_user_from_context(context, userRef)
    groups = list_user_group(context.session, host=context.config.userdata.get("target"), userId=user['header']['id'])
    
    #only applicable to org groups
    org_gids = []
    if "orgs" in context.table.headings:
        org_gids = set([get_relative_org(context, int(x["orgs"]))["allGroupUserId"] for x in context.table])
    

    #only applicable to groups
    all_groups=set()
    if "groups" in context.table.headings:
        all_groups = set([get_group_from_context(context, x["groups"])["header"]["id"] for x in context.table])

    allg = list(all_groups.union(org_gids))
    allg.sort()


    gids = [g['header']['id'] for g in groups]
    gids.sort()

    print(f"expected groups: {allg}", file=sys.stderr)
    print(f"fetched groups: {gids}", file=sys.stderr)

    assert allg == gids

@then('I change user {userRef} to state "{state}"')
def change_user_state(context, userRef, state):
    user = get_user_from_context(context, userRef)
    user["state"] = state
    update_user(
        session = context.session,
        host = context.config.userdata.get("target"),
        user = user
    )

@then('I check for user {userRef} state is "{state}"')
def check_user_state(context, userRef, state):
    user = get_user_from_context(context, userRef)
    user = get_user(session = context.session,
        host = context.config.userdata.get("target"),
        username = user["header"]["name"])

    update_user_in_context(
        context=context,
        userRef=userRef,
        user = user
    )

    if not user['state'] == state:
        print(user)
        assert False
