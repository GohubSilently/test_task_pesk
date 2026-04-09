import time

from redis.asyncio import Redis

from .config import settings


redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True
)


async def whitelist_add_token(jti: str, user_id: int, expired: int = settings.jwt_access_token_exp):
    await redis.set(name=f'whitelist:{jti}', value=user_id, ex=expired)


async def whitelist_check_token(jti: str) -> bool:
    return await redis.exists(f'whitelist:{jti}')


async def whitelist_delete_token(jti: str):
    return await redis.delete(f'whitelist:{jti}')


async def blacklist_add_token(jti: str, user_id: int, expired: int = settings.jwt_access_token_exp):
    ttl = expired - int(time.time())
    if ttl > 0:
        await redis.set(name=f'blacklist:{jti}', value=user_id, ex=ttl)


async def blacklist_check_token(jti: str) -> bool:
    return await redis.exists(f'blacklist:{jti}')
