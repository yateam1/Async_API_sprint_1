from datetime import date
from typing import Optional, List

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    actor: Optional[List[str]] = []
    director: Optional[List[str]] = []
    writer: Optional[List[str]] = []
    producer: Optional[List[str]] = []
