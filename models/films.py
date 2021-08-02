from datetime import date
from typing import List, Optional

from models.base import BaseModel
from models.constants import FilmWorkTypeEnum


class Film(BaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.movie
    creation_date: date
    genres: Optional[List[str]] = []
    rating: float = 0.0
    directors: Optional[List[str]] = []
    actors: Optional[List[str]] = []
    writers: Optional[List[str]] = []
    producers: Optional[List[str]] = []

