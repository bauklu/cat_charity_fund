from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser, current_user
from app.models import User
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.services.investment import invest_funds
from app.schemas.donation import (
    DonationCreate, DonationAdminRead, DonationUserRead
)

router = APIRouter()


async def after_create_donation(_: Donation, session: AsyncSession):
    await invest_funds(session)


@router.post(
    '/',
    response_model=DonationUserRead,
    response_model_exclude={
        'user_id',
    },
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation,
        session,
        user,
        after_create=after_create_donation
    )
    return new_donation


@router.get(
    '/',
    response_model=list[DonationAdminRead],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationUserRead],
    response_model_exclude={'user_id'},
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Получает список всех пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
