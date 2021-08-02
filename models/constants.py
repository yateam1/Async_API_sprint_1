from enum import Enum


class FilmWorkTypeEnum(str, Enum):
    """Варианты типов кинопроизведений."""

    movie = 'movie'
    serial = 'serial'
