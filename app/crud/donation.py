from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    """
    Класс для выполнения операций CRUD
    над моделями пожертвований.
    """

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ) -> list[Donation]:
        """Возвращает список пожертвований конкретного пользователя."""
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def get_future_donations_for_project(
        self,
        project_id: int,
        session: AsyncSession
    ):
        result = await session.execute(
            select(Donation).where(Donation.charity_project_id == project_id)
        )
        return result.scalars().all()

    async def get_not_fully_invested(self, session: AsyncSession):
        result = await session.execute(
            select(Donation).where(
                Donation.fully_invested.is_(False)
            ).order_by(Donation.create_date)
        )
        return result.scalars().all()

    async def add_to_session(
        self,
        db_obj: Donation,
        session: AsyncSession
    ) -> None:
        session.add(db_obj)


donation_crud = CRUDDonation(Donation)
