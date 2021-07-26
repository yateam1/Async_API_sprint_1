from datetime import datetime
from typing import List

from models.base import BaseModel
from models.constants import FilmWorkTypeEnum
from models import Genre, Person


class Film(BaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.movie
    creation_date: datetime
    genres: List[Genre] = []
    rating: float = 0.0
    directors: List[Person] = []
    actors: List[Person] = []
    writers: List[Person] = []
    producers: List[Person] = []

