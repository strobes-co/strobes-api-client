import requests
from strobes_client import enums
from strobes_client.exceptions import EmailException, PasswordException
from strobes_client.helpers import get_jwt_token
from strobes_client.enums import RequestEnums

class BaseClient:
    def __init__(self, email: str = None, password: str = None,
                 host: str = RequestEnums.app_host.value, port: int = RequestEnums.app_port.value,
                 scheme: str = RequestEnums.app_scheme.value, api_token: str = None, verify: bool = True):
        self.app_url = f"{scheme}://{host}:" \
            f"{str(port)}/"
        if not api_token:
            if not email:
                raise EmailException
            if not password:
                raise PasswordException
            token = get_jwt_token(self.app_url, email, password)
            self.s = requests.Session()
            self.s.verify = verify
            self.s.headers.update({"Authorization": f"JWT {token}",
                                "user-agent": RequestEnums.user_agent.value})
        else:
            self.s = requests.Session()
            self.s.verify = verify
            self.s.headers.update({"Authorization": f"{api_token}",
                                "user-agent": RequestEnums.user_agent.value})
