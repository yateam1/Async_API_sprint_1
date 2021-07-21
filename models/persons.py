from datetime import datetime
from typing import Optional

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
