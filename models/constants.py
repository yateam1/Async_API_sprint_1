from enum import Enum


class FilmWorkTypeEnum(str, Enum):
    """Варианты типов кинопроизведений."""

    movie = 'Фильм'
    series = 'Сериал'
    tv_show = 'Тв-шоу'
