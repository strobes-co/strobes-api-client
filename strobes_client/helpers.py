import requests
from strobes_client.exceptions import LoginFailure, ResourceException, UnexpectedStatusCode


def get_jwt_token(url: str, email: str, password: str) -> str:
    r = requests.post(f"{url}api/v1/login/",
                      json={"email": email, "password": password})
    resp = r.json()
    if 'access' in resp:
        return resp['access']
    if 'otp_type' in resp:
        raw_otp = input('Enter OTP: ')
        r = requests.post(f"{url}api/v2/verify-otp/", json={"email": email, "password": password, "otp": raw_otp})
        resp = r.json()
        if 'access' in resp:
            return resp['access']
    raise LoginFailure


def check_keys(data: dict, keys: list, optional: list):
    for k in keys:
        if k not in data and k not in optional:
            raise ResourceException(f'{k} not availabe')


def check_status_code(r: requests.Response):
    if r.status_code not in [200, 201]:
        raise UnexpectedStatusCode
