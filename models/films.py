from datetime import date

from models.base import BaseModel
from models.constants import FilmWorkTypeEnum


class Film(BaseModel):
    """Описание модели кинопроизведения."""
    title: str
    description: str
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.movie
    creation_date: date
    rating: float = 0.0
    age_classification: int = 0
    by_subscription: bool = False
    genres: list[str] = []
    directors: list[str] = []
    actors: list[str] = []
    writers: list[str] = []
    producers: list[str] = []

