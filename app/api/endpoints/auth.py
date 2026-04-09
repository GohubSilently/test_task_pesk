from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.core.config import settings
from app.core.db import (
    blacklist_add_token,
    blacklist_check_token,
    whitelist_add_token,
    whitelist_check_token,
    whitelist_delete_token
)

from app.core.utils import create_token, decode_token


router = APIRouter()


USERS = {
    'user': {
        'id': 1,
        'password': 'user',
        'role': 'user'
    },
    'moderator': {
        'id': 2,
        'password': 'moderator',
        'role': 'moderator'
    },
    'admin': {
        'id': 3,
        'password': 'admin',
        'role': 'admin'
    },
}


@router.post('/login')
async def login(data: dict) -> dict[str, str]:
    username = data.get('username')
    password = data.get('password')

    user = USERS.get(username)

    if not user or user['password'] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Дожны быть поля username и пароль!'
        )

    access_token, access_jti = create_token(
        user['id'], user['role'], 'access'
    )
    refresh_token, refresh_jti = create_token(
        user['id'], user['role'], 'refresh', settings.jwt_refresh_token_exp
    )
    await whitelist_add_token(access_jti, user['id'])
    await whitelist_add_token(refresh_jti, user['id'], settings.jwt_refresh_token_exp)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


@router.post('/logout')
async def logout(user=Depends(get_current_user)) -> dict[str, str]:
    await blacklist_add_token(user['jti'], user['user_id'], user['exp'])
    await whitelist_delete_token(user['jti'])
    return {'message': 'Вы успешно разлогинились!'}


@router.post("/refresh")
async def refresh(data: dict) -> dict[str, str]:
    payload = decode_token(data.get('refresh_token'))

    if not payload or payload['type'] != 'refresh':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Ошибка в поле refresh_token'
        )

    if await blacklist_check_token(payload['jti']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен в черном списке'
        )

    if not await whitelist_check_token(payload['jti']):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Токена нет в белом списке'
        )
    await whitelist_delete_token(payload["jti"])

    access_token, access_jti = create_token(
        payload['user_id'], payload['role'], 'access'
    )
    refresh_token, refresh_jti = create_token(
        payload['user_id'], payload['role'], 'refresh', settings.jwt_refresh_token_exp
    )

    await whitelist_add_token(access_jti, payload['user_id'])
    await whitelist_add_token(refresh_jti, payload['user_id'], settings.jwt_refresh_token_exp)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
