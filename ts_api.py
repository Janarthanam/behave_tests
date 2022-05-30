from array import array
import re
from urllib import response
from urllib.error import HTTPError
import requests
import sys
import os
import json
import urllib.parse
from utils import log_raise_for_status

def login(host: str, user: str, password: str) -> None:
    session = requests.session()
    post_data = {'username': user, 'password': password, 'rememberme' : True}
    response = session.post(f"{host}/callosum/v1/session/login", data = post_data)
    #print(json.dumps(response.json(), indent=3))
    log_raise_for_status(response)
    return session

def get_auth_token(host: str, user: str, secret_key: str, orgId: int = None) -> str: 
    post_data = {'secret_key': secret_key, 'username': user, 'access_level': 'FULL', 'orgid': orgId}
    response = requests.post(f"{host}/callosum/v1/session/auth/token", data = post_data)
    log_raise_for_status(response)
    print(f"get_auth_token {response.text}")
    return response.text

def login_as_user(host: str, user: str, token: str, redirect_host: str):
    session = requests.session()
    get_data = {'username':user, 'auth_token': token, 'redirect_url': f"{redirect_host}"}
    response = session.get(f"{host}/callosum/v1/session/login/token", params = get_data, allow_redirects=False)
    print(f"login_as_user {response.cookies}")
    log_raise_for_status(response)
    return session

def session_info(session, host: str) -> dict:
    response = session.get(f"{host}/callosum/v1/session/info")
    log_raise_for_status(response)
    session_info = response.json()
    return session_info

def session_orgs(session: requests.Session, host: str) -> dict:
    response = session.get(f"{host}/callosum/v1/session/orgs")
    print(response.text)
    log_raise_for_status(response)
    return response.json()

def switch_org(session: requests.Session, host: str, orgId: int):
    put_data = {"org" : orgId}
    response = session.put(f"{host}/callosum/v1/session/orgs", data = put_data)
    log_raise_for_status(response)
    return response

def create_user(session, host: str, username: str, orgId: int = None, groups: list[str] = None):
    post_data = {'name' : username, 'password': "Whatever123!@", 'orgid': orgId, 'displayname': username, 'groups': json.dumps(groups)}
    response = session.post(f"{host}/callosum/v1/session/user/create", data = post_data)
    #print(json.dumps(response.json(), indent=3))
    log_raise_for_status(response)
    return response.json()

def get_user(session, host: str, username: str):
    get_params = {'name' : username}
    response = session.get(f"{host}/callosum/v1/tspublic/v1/user", params = get_params)
    log_raise_for_status(response)
    return response.json()

def update_user(session, host: str, user, orgIds: list[int] = [], groups: list[str] = []):
    if (not orgIds is None) and len(orgIds) > 0 :
        user["header"]["orgIds"] = orgIds

    if (not groups is None) and len(groups) > 0:
        user["assignedGroups"] = groups
    
    update_body = {"userid": f"{user['header']['id']}", "content": json.dumps(user)}
    print(update_body)
    response = session.post(f"{host}/callosum/v1/session/user/update", data = update_body)
    print(response.text)
    log_raise_for_status(response)
    return response

def delete_user(session, host: str, user_id: str, orgId: int = None):
    params = {'orgid' : orgId}
    response = session.delete(f"{host}/callosum/v1/session/user/delete/{user_id}", params = params)
    #print(response.request.body)
    log_raise_for_status(response)
    return response

def list_user_group(session, host: str, userId: str):
    response = session.get(f"{host}/callosum/v1/session/user/listgroup/{userId}")
    #print(json.dumps(response.json(), indent=3))
    log_raise_for_status(response)
    return [x for x in response.json()]

def get_users_in_group(session, host:str, groupId: str):
    response = session.get(f"{host}/callosum/v1/session/group/listuser/{groupId}")
    #print(json.dumps(response.json(), indent=3))
    log_raise_for_status(response)
    return [x['header']['name'] for x in response.json()]

def add_user_to_group(session, host: str, userId: str, group: str):
    post_data = {"userid": userId, "groupid": group}
    response = session.post(f"{host}/callosum/v1/session/group/adduser", data = post_data)
    #print(response.text)
    log_raise_for_status(response)
    return response

def session_org_info(session, host: str):
    response = session.get(f"{host}/callosum/v1/session/orgs")
    log_raise_for_status(response)
    return response.json() 

#todo: wip
def _scrape_recursively(session, path: str) -> dict:
    response = session.get(path)
    log_raise_for_status(response)
    docs = {}
    paths = response.json()
    apis = [x for x in paths["apis"]]
    for api in apis:
        if (api.get("operations") == None):
            t = _scrape_recursively(session, path=f"{path}{api['path']}")
            docs.update(t)
        else:
            docs.update(api)
    return docs

def get_api_doc(session, host: str):
    return _scrape_recursively(session, f"{host}/callosum/v1/api-docs")

def create_group(session, host:str, name: str, org_id: int):
    post_body = {'name': name, 'display_name': name, 'orgid': org_id }
    return _session_calls(lambda: session.post(f"{host}/callosum/v1/session/group/create", data = post_body))

def _session_calls(f) -> requests.Response:
    try:
        response = f()
    except HTTPError as ex:
        print(response.text)
        raise ex
    return response.json()



class Orgs:
    def __init__(self, session: requests.Session, host: str):
        self.session = session
        self.host = host

    def create_org(self, name: str, description: str) -> dict:
        post_data = {'name': name, 'description': description}
        response = self.session.post(f"{self.host}/callosum/v1/org/create", data = post_data)
        print(response.text)
        #print(json.dumps(response.json(), indent = 3))
        #print(response.request.body)
        log_raise_for_status(response)
        return response.json()

    def delete_org(self, orgId: int) -> requests.Response:
        response = self.session.delete(f"{self.host}/callosum/v1/org/delete/{orgId}")
        log_raise_for_status(response)
        return response

