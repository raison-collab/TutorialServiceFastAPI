from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from config import TOKEN_SECRET

cookie_transport = CookieTransport(
    cookie_name='TutoringServiceFastAPIAuth',
    cookie_max_age=3600,  # токен выдается на час
    cookie_secure=False,
    cookie_samesite='none'
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=TOKEN_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
