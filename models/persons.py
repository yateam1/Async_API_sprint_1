from datetime import datetime
from typing import Optional, List

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    actor: List[str] = []
    director: List[str] = []
    writer: List[str] = []
    producer: List[str] = []
