from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, Field, validator


class CharityProjectCreate(BaseModel):
    """Схема при создании нового благотворительного проекта."""
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    full_amount: conint(gt=0)  # type: ignore


class CharityProjectUpdate(BaseModel):
    """Схема при редактировании благотворительного проекта."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[conint(gt=0)] = None  # type: ignore

    @validator('name')
    def name_cannot_be_null(cls, value):
        """
        Проверка на наличие названия при обновлении
        благотворительного проекта.
        """
        if value == '':
            raise ValueError('Название проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    """Схема для чтения данных благотворительного проекта из базы данных."""
    id: int
    fully_invested: bool
    invested_amount: int
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
