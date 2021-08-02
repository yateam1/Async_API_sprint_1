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
    genres: Optional[List[str]] = [] # Список названий жанров
    directors: Optional[List[str]] = [] # Список имен режиссеров
    actors: Optional[List[str]] = [] # Список названий актёров
    writers: Optional[List[str]] = [] # Список названий сценаристов
    producers: Optional[List[str]] = [] # Список названий продюсеров

