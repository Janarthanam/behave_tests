import behave

def get_user_from_context(context, userRef):
    return context.users[int(userRef)] if (isinstance(userRef, int)) else context.users[-1]

def get_relative_orgId(context, orgNo:int) -> int: 
    return context.orgs[int(orgNo)-1]["orgId"]

def get_host(context)->str:
    return context.config.userdata.get("target")