from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

from .db import blacklist_check_token, whitelist_check_token
from .utils import decode_token


security = HTTPBearer()


async def get_current_user(credentials=Depends(security)) -> dict[str, Any]:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Недействительный или истекший токен'
        )
    if await blacklist_check_token(payload['jti']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен в черном листе'
        )
    if not await whitelist_check_token(payload['jti']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неизвестный токен'
        )
    return payload
