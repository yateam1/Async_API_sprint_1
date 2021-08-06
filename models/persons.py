from datetime import date
from typing import Optional
from uuid import UUID

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    actor: list[UUID] = []
    director: list[UUID] = []
    writer: list[UUID] = []
    producer: list[UUID] = []
