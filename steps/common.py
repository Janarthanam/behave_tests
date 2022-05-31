import behave

def get_user_from_context(context, userRef):
    return context.users[int(userRef)] if (isinstance(userRef, int)) else context.users[-1]

def get_relative_org(context, orgNo:int) -> dict:
    #todo: org 0 should return real 0 org.
    return context.orgs[int(orgNo)-1]

def get_group_from_context(context, groupRef):
    if groupRef is None:
        return []
    return context.groups[int(groupRef)] if (isinstance(groupRef, int)) else context.groups[-1]

def get_relative_org_id(context, orgNo) -> int:
    if orgNo is None:
        return None 
    return get_relative_org(context, int(orgNo))["orgId"]

def get_host(context)->str:
    return context.config.userdata.get("target")

def get_password(context)->str:
    return context.config.userdata.get("passwd")

def get_users(context)->list:
    if not "users" in context:
        context.users=[] 
    return context.users

def get_groups(context)->list:
    if not "groups" in context:
        context.groups=[]
    return context.groups
