from fastapi import APIRouter, Depends

from app.core.auth import get_current_user
from app.core.roles import require_role

router = APIRouter()


@router.get('/user')
async def common(user=Depends(get_current_user)) -> dict[str, str]:
    return {'message': 'Общий контент для всех'}


@router.get('/moderator')
async def manager_admin(user=Depends(require_role('moderator', 'admin'))) -> dict[str, str]:
    return {'message': 'Контент для модераторов и админов'}


@router.get('/admin')
async def admin(user=Depends(require_role('admin'))) -> dict[str, str]:
    return {'message': 'Контент только для админа'}
