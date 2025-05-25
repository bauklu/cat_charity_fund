from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject, Donation, User
from app.crud.donation import donation_crud


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_name_duplicate_on_update(
    project_id: int,
    new_name: str,
    session: AsyncSession
):
    result = await session.execute(
        select(CharityProject).where(CharityProject.name == new_name)
    )
    existing_project = result.scalars().first()
    if existing_project and existing_project.id != project_id:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует."
        )


async def check_donation_before_edit(
        donation_id: int,
        session: AsyncSession,
        user: User,
) -> Donation:
    donation = await donation_crud.get(
        obj_id=donation_id, session=session
    )
    if not donation:
        raise HTTPException(
            status_code=404,
            detail='Пожертвование не найдено!'
        )
    if donation.user_id != user.id and not user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужое пожертвование!'
        )
    return donation


def validate_full_amount(
    db_obj: CharityProject,
    new_full_amount: int
) -> None:
    if new_full_amount < db_obj.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше уже вложенной суммы.'
            )
        )


def check_project_not_invested(project: CharityProject) -> None:
    """Проверяет, что в проект не инвестировали средства."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя удалить проект, '
                'в который уже были внесены средства.'
            )
        )


def check_project_not_closed(project: CharityProject) -> None:
    """Проверяет, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать.'
        )
