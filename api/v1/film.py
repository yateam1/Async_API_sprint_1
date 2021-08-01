from datetime import datetime
import json
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    # id: str
    title: str
    description: str
    type: str


@router.get('/all', response_model=List[Film])
async def movies_list(film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    """
    Предоставляет информацию о всех фильмах
    """
    films = await film_service._get_all()
    return films
    # return paginate(films)
    # raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
    Предоставляет информацию о кинопроизведении по его id
    :param film_id:
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться уже определёнными HTTP-статусами, которые содержат enum
                # Такой код будет более поддерживаемым
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    # Перекладываем данные из models.Film в Film
    # Обратите внимание, что у модели бизнес-логики есть поле description
        # Которое отсутствует в модели ответа API.
        # Если бы использовалась общая модель для бизнес-логики и формирования ответов API
        # вы бы предоставляли клиентам данные, которые им не нужны
        # и, возможно, данные, которые опасно возвращать
    out = json.loads(film.json())
    return Film(**out)