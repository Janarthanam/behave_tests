from array import array
import re
from urllib import response
import requests
import sys
import os
import json
import urllib.parse

def login(host: str, user: str, password: str) -> None:
    session = requests.session()
    post_data = {'username': user, 'password': password, 'rememberme' : True}
    response = session.post(f"{host}/callosum/v1/session/login", data = post_data)
    #print(response.request.body)
    response.raise_for_status()
    return session

def get_auth_token(host: str, user: str, secret_key: str, orgId: int = None) -> str: 
    post_data = {'secret_key': secret_key, 'username': user, 'access_level': 'FULL', 'orgid': orgId}
    response = requests.post(f"{host}/callosum/v1/session/auth/token", data = post_data)
    response.raise_for_status()
    print(f"get_auth_token {response.text}")
    return response.text

def login_as_user(host: str, user: str, token: str, redirect_host: str):
    session = requests.session()
    get_data = {'username':user, 'auth_token': token, 'redirect_url': f"{redirect_host}"}
    response = session.get(f"{host}/callosum/v1/session/login/token", params = get_data, allow_redirects=False)
    print(f"login_as_user {response.cookies}")
    response.raise_for_status()
    return session

def session_info(session, host: str) -> dict:
    response = session.get(f"{host}/callosum/v1/session/info")
    response.raise_for_status()
    session_info = response.json()
    return session_info

def session_orgs(session: requests.Session, host: str) -> dict:
    response = session.get(f"{host}/callosum/v1/session/orgs")
    response.raise_for_status()
    return response.json()

def switch_org(session: requests.Session, host: str, orgId: int):
    put_data = {"org" : orgId}
    response = session.put(f"{host}/callosum/v1/session/orgs", data = put_data)
    print(response.text)
    response.raise_for_status()
    return response

def create_user(session, host: str, username: str, orgId: int = None):
    post_data = {'name' : username, 'password': "Whatever123", 'orgid': orgId, 'displayname': username}
    response = session.post(f"{host}/callosum/v1/session/user/create", data = post_data)
    #print(json.dumps(response.json(), indent=3))
    response.raise_for_status()
    return response.json()

def get_user(session, host: str, username: str):
    get_params = {'name' : username}
    response = session.get(f"{host}/callosum/v1/tspublic/v1/user", params = get_params)
    response.raise_for_status()
    return response.json()

def update_user(session, host: str, user, orgIds: list[int] = [], groups: list[str] = []):
    if len(orgIds) > 0 :
        user["header"]["orgIds"] = orgIds

    if len(groups) > 0:
        user["assignedGroups"] = groups
    
    update_body = {"content": str(user)}
    print(update_body)
    response = session.post(f"{host}/callosum/v1/tspublic/v1/user/{user['header']['id']}", data = update_body)
    response.raise_for_status()
    return response

def delete_user(session, host: str, user_id: str, orgId: int = None):
    params = {'orgid' : orgId}
    response = session.delete(f"{host}/callosum/v1/session/user/delete/{user_id}", params = params)
    print(response.request.body)
    response.raise_for_status()
    return response

def list_user_group(session, host: str, userId: str):
    response = session.get(f"{host}/callosum/v1/session/user/listgroup/{userId}")
    print(json.dumps(response.json(), indent=3))
    response.raise_for_status()

def session_org_info(session, host: str):
    response = session.get(f"{host}/callosum/v1/session/orgs")
    response.raise_for_status()
    return response.json() 

class Orgs:
    def __init__(self, session: requests.Session, host: str):
        self.session = session
        self.host = host

    def create_org(self, name: str, description: str) -> dict:
        post_data = {'name': name, 'description': description}
        response = self.session.post(f"{self.host}/callosum/v1/org/create", data = post_data)
        print(json.dumps(response.json(), indent = 3))
        print(response.request.body)
        response.raise_for_status()
        return response.json()

    def delete_org(self, orgId: int) -> requests.Response:
        response = self.session.delete(f"{self.host}/callosum/v1/org/delete/{orgId}")
        response.raise_for_status()
        return response

