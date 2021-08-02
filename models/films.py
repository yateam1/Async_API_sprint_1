from datetime import date
from typing import List

from models.base import BaseModel
from models.constants import FilmWorkTypeEnum


class Film(BaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.movie
    creation_date: date
    genres: List[str] = []
    rating: float = 0.0
    directors: List[str] = []
    actors: List[str] = []
    writers: List[str] = []
    producers: List[str] = []

