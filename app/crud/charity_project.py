from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    """
    Класс для выполнения операций CRUD
    над моделями благотворительных проектов.
    """

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Возвращает id проекта по его имени. """
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_not_fully_invested(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested.is_(False)
            ).order_by(CharityProject.create_date)
        )
        return project.scalars().all()

    async def add_to_session(
        self,
        db_obj: CharityProject,
        session: AsyncSession
    ) -> None:
        session.add(db_obj)


charity_project_crud = CRUDCharityProject(CharityProject)
