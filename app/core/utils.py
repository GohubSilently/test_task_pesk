import uuid
from datetime import datetime, timedelta, UTC
from typing import Any

import jwt

from .config import settings


def create_token(user_id: int, role: str, token_type: str, expired: int = settings.jwt_access_token_exp) -> tuple[str, str]:
    jti = str(uuid.uuid4())

    payload = {
        'user_id': user_id,
        'role': role,
        'type': token_type,
        'jti': jti,
        'iat': datetime.now(UTC),
        'exp': datetime.now(UTC) + timedelta(seconds=expired),
    }

    token = jwt.encode(payload, settings.jwt_secret_key, settings.jwt_algorithm)
    return token, jti


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
    except jwt.exceptions.InvalidTokenError:
        return None
