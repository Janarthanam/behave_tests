from ts_api import *
from behave import *
from utils import *
from requests import *

@when('The tenant has {n} orgs')
@when('I create {n} more orgs')
def create_orgs(context, n):
    orgs = Orgs(context.session, host=context.config.userdata.get("target"))
    context.orgs = []
    try:
        for i in range(0,int(n)):
            org = orgs.create_org(name = random_str(), description= random_str())
            print("Creating org" + str(i))
            context.orgs.append(org)
    except HTTPError as error:
        print(error)
        context.error=error

