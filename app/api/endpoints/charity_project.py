from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject  # noqa
from app.models.user import User  # noqa
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import invest_funds
from app.schemas.donation import DonationAdminRead
from app.api.validators import (
    check_name_duplicate, check_project_name_duplicate_on_update,
    check_charity_project_exists, validate_full_amount,
    check_project_not_invested,
    check_project_not_closed
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)

    async def after_create_func(_, session):
        await invest_funds(session)

    return await charity_project_crud.create(
        charity_project,
        session,
        after_create=after_create_func
    )


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
    status_code=HTTPStatus.OK
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if obj_in.name:
        await check_project_name_duplicate_on_update(
            charity_project_id, obj_in.name, session
        )

    check_project_not_closed(charity_project)

    if obj_in.full_amount is not None:
        validate_full_amount(charity_project, obj_in.full_amount)

    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    check_project_not_invested(charity_project)

    return await charity_project_crud.remove(
        charity_project,
        session
    )


@router.get(
    '/{charity_project_id}/donations',
    response_model=list[DonationAdminRead],
    response_model_exclude={'user_id'},
)
async def get_donations_for_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_exists(
        charity_project_id, session
    )
    return await donation_crud.get_future_donations_for_project(
        project_id=charity_project_id, session=session)
