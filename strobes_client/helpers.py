import requests
from strobes_client.exceptions import LoginFailure, ResourceException


def get_jwt_token(url: str, email: str, password: str) -> str:
    r = requests.post(f"{url}api/v1/login/",
                      json={"email": email, "password": password})
    resp = r.json()
    if 'token' in resp:
        return resp['token']
    raise LoginFailure


def check_keys(data: dict, keys: list):
    for k in keys:
        if k not in data:
            raise ResourceException(f'{k} not availabe')
