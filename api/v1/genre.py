from http import HTTPStatus
from typing import Tuple

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    name: str


# Внедряем GenreService с помощью Depends(get_genre_service)
@router.get('/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
    Предоставляет информацию о жанре по его id
    :param genre_id:
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        # Если жанр не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    # Перекладываем данные из models.genre в genre
    # Обратите внимание, что у модели бизнес-логики есть поле description
        # Которое отсутствует в модели ответа API.
        # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
        # вы бы предоставляли клиентам данные, которые им не нужны
        # и, возможно, данные, которые опасно возвращать
    return Genre(id=genre.id, name=genre.name)


@router.get('', response_model=Genre)
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> Tuple[Genre]:
    """
    Предоставляет информацию о всех жанрах
    :param genre_id:
    """
    pass
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genres not found')
