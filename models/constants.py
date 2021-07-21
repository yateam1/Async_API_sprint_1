from enum import Enum


class FilmWorkTypeEnum(str, Enum):
    """Варианты типов кинопроизведений."""

    movie = 'Фильм'
    serial = 'Сериал'
