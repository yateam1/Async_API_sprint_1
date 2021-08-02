from datetime import date
from typing import Optional, List
from uuid import UUID

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    actor: Optional[List[UUID]] = []
    director: Optional[List[UUID]] = []
    writer: Optional[List[UUID]] = []
    producer: Optional[List[UUID]] = []
