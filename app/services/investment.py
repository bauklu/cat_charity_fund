from datetime import datetime
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def invest_funds(session: AsyncSession):
    """
    Автоматически распределяет средства между открытыми проектами
    и активными пожертвованиями.
    """
    projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(CharityProject.create_date)
    )
    projects = projects.scalars().all()

    donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(Donation.create_date)
    )
    donations = donations.scalars().all()

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
            session.add(project)
            session.add(donation)
