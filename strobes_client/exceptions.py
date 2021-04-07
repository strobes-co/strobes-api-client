class JWTRequired(Exception):
    def __str__(self):
        return "JWT is require."


class EmailException(Exception):
    def __str__(self):
        return "Username is required."


class PasswordException(Exception):
    def __str__(self):
        return "Password is required."


class LoginFailure(Exception):
    def __str__(self):
        return "Failed to login."


class ResourceException(Exception):
    pass


class UnexpectedStatusCode(Exception):
    def __str__(self):
        return "response returned an unexpected status code other than 2xx"
