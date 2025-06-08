from datetime import timedelta
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from constants import (SECONDS_IN_DAY,
                       SECONDS_IN_HOUR,
                       SECONDS_IN_MINUTE,
                       MICROSECONDS_WIDTH,
                       WIDTH
                       )
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

    async def get_project_by_completion_rate(
            self, session: AsyncSession
    ) -> List[dict]:
        duration_expr = (
            (
                func.julianday(CharityProject.close_date) -
                func.julianday(CharityProject.create_date)
            ) * SECONDS_IN_DAY
        ).label('duration_seconds')

        stmt = (
            select(
                CharityProject.name,
                CharityProject.description,
                duration_expr
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by('duration_seconds')
        )

        result = await session.execute(stmt)
        rows = result.all()

        def format_duration(delta: timedelta) -> str:
            days = delta.days
            hours, remainder = divmod(delta.seconds, SECONDS_IN_HOUR)
            minutes, seconds = divmod(remainder, SECONDS_IN_MINUTE)
            return (
                f"{days} day{'s' if days != 1 else ''}, "
                f"{hours:0{WIDTH}}:{minutes:0{WIDTH}}:{seconds:0{WIDTH}}."
                f"{delta.microseconds:0{MICROSECONDS_WIDTH}}"
            )

        projects = []
        for name, description, duration_seconds in rows:
            try:
                duration = timedelta(seconds=float(duration_seconds))
            except (TypeError, ValueError):
                duration = timedelta(seconds=0)

            projects.append({
                'charityproject_name': name,
                'duration': format_duration(duration),
                'charityproject_description': description
            })

        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
