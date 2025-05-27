from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject  # noqa
from app.models.donation import Donation  # noqa


async def invest_funds(session: AsyncSession):
    """
    Автоматически распределяет средства между открытыми проектами
    и активными пожертвованиями.
    """
    projects = await charity_project_crud.get_not_fully_invested(session)

    donations = await donation_crud.get_not_fully_invested(session)

    for project in projects:
        for donation in donations:
            if project.fully_invested:
                break
            if donation.fully_invested:
                continue

            need = project.full_amount - project.invested_amount
            available = donation.full_amount - donation.invested_amount
            transfer = min(need, available)

            project.invested_amount += transfer
            donation.invested_amount += transfer

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()

            await charity_project_crud.add_to_session(project, session)
            await donation_crud.add_to_session(donation, session)
