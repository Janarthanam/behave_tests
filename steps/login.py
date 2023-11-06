from create_user_in_org import login_using_secret
from ts_api import *
from utils import *
from common import *

@given("A tenant admin user")
@given("I am a tenant admin")
def login_as_admin(context):
    context.session = login(host=get_host(context),user="tsadmin",password="admin")
    switch_org(context.session, host=get_host(context), orgId=-1)


@given('I am an org admin for org {org}')
@given('I switch to org {org}')
def org_admin(context, org):
    print(f"{org} number of orgs. {len(context.orgs)}")
    switch_org(context.session, host=get_host(context), orgId=get_relative_orgId(context, org))

@when('I try to login using {tokenRef} token in to "{username}"')
def login_using_token(context, tokenRef, username):
    context.session = login_as_user(host=get_host(context), user=username, token=context.token, redirect_host=get_host(context))

@Then('I get an user token for "{username}" using secret in org {org}')
def generate_token(context, username, org: int):
    context.token = get_auth_token(host=get_host(context), user=username, secret_key=context.config.userdata.get("secret"), orgId=get_relative_orgId(context,org))


@Then('I should be logged in to org {org}')
def logged_into(context, org):
    orgs = session_orgs(context.session,host=get_host(context))
    assert orgs["currentOrgId"] == get_relative_orgId(context,org)

