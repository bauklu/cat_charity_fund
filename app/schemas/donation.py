from typing import Optional
from datetime import datetime

from pydantic import BaseModel, conint


class DonationBase(BaseModel):
    """Схема для чтения данных пожертвования."""

    comment: Optional[str] = None
    full_amount: conint(gt=0)  # type: ignore


class DonationCreate(DonationBase):
    """Схема при создании нового пожертвования."""

    pass


class DonationUserRead(DonationBase):
    """Схема для чтения данных пожертвования для обычного пользователя."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


# Для администратора
class DonationAdminRead(DonationUserRead):
    """Схема для чтения данных пожертвования для суперпользователя."""

    id: int
    user_id: int
    fully_invested: bool
    invested_amount: conint(ge=0)  # type: ignore
    close_date: Optional[datetime] = None
    create_date: datetime

    class Config:
        orm_mode = True
