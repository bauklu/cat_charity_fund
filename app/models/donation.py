"""Модель пожертвования."""

from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import AbstractInvestment


class Donation(AbstractInvestment):
    """Модель для хранения информации о пожертвованиях пользователей."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
    charity_project_id = Column(
        Integer,
        ForeignKey('charityproject.id'),
        nullable=True
    )
    user = relationship('User', back_populates='donations')
    project = relationship('CharityProject', back_populates='donations')
