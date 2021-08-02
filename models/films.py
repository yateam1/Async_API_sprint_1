from datetime import date
from typing import List, Optional
from uuid import UUID

from models.base import BaseModel
from models.constants import FilmWorkTypeEnum


class Film(BaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.movie
    creation_date: date
    rating: float = 0.0
    genres: Optional[List[str]] = []
    directors: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    writers: Optional[List[str]] = []
    producers: Optional[List[str]] = []

