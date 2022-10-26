from datetime import timedelta
from blacksheep import Request
import jwt
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from rodi import Services


AccessToken = str
RefreshToken = str
Token = AccessToken | RefreshToken
TokenPayload = dict


class JWTManager:
    def __init__(self, key: str, algorithm: str) -> None:
        self._key = key
        self._algorithm = algorithm

    def verify_token(self, token: Token) -> bool:
        verified = True
        try:
            decoded = jwt.decode(token, self._key, algorithms=[self._algorithm])
            if "sub" not in decoded:
                raise jwt.exceptions.InvalidTokenError()
        except jwt.exceptions.PyJWTError:
            verified = False

        return verified

    def get_payload(self, token: Token) -> TokenPayload:
        return jwt.decode(token, self._key, algorithms=[self._algorithm])

    def generate_access_token(
        self, sub: str, ex: timedelta | None = None
    ) -> AccessToken:
        ex = ex or timedelta(minutes=30)
        payload = {"ex": ex, "sub": sub}
        return jwt.encode(payload, self._key, self._algorithm)

    def generate_refresh_token(
        self, sub: str, ex: timedelta | None = None
    ) -> RefreshToken:
        ex = ex or timedelta(days=7)
        payload = {"ex": ex, "sub": sub}
        return jwt.encode(payload, self._key, self._algorithm)

    def update_access_token(self, refresh_token: RefreshToken) -> AccessToken | None:
        if not self.verify_token(refresh_token):
            return None

        payload = self.get_payload(refresh_token)
        sub = payload["sub"]

        return self.generate_access_token(sub)


class JWTAuthHandler(AuthenticationHandler):
    def __init__(self, provider: Services) -> None:
        self._provider = provider

    async def authenticate(self, context: Request) -> Identity | None:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            jwt_manager = self._provider.get(JWTManager)
            parts = header_value.split()
            if len(parts) != 2:
                return None

            token = parts[1]
            if not jwt_manager.verify_token(token):
                return None

            payload = jwt_manager.get_payload(token)
            context.identity = Identity(payload, "JWT")
        else:
            context.identity = None
        return context.identity
