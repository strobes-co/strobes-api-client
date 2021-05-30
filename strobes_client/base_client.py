import requests
from strobes_client import enums
from strobes_client.exceptions import EmailException, PasswordException
from strobes_client.helpers import get_jwt_token


class BaseClient:
    def __init__(self, email: str = None, password: str = None,
                 host: str = enums.APP_HOST, port: int = enums.APP_PORT,
                 scheme: str = enums.APP_SCHEME, api_token: str = None):
        self.app_url = f"{scheme}://{host}:" \
            f"{str(port)}/"
        if not api_token:
            if not email:
                raise EmailException
            if not password:
                raise PasswordException
            token = get_jwt_token(self.app_url, email, password)
            self.s = requests.Session()
            self.s.headers.update({"Authorization": f"JWT {token}",
                                "user-agent": enums.USER_AGENT})
        else:
            self.s = requests.Session()
            self.s.headers.update({"Authorization": f"{api_token}",
                                "user-agent": enums.USER_AGENT})
