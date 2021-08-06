from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_cache.decorator import cache

from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


# Внедряем GenreService с помощью Depends(get_genre_service)
@router.get('/{genre_id}', response_model=Genre)
@cache(expire=3600)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    """
    Предоставляет информацию о жанре по его id
    :param genre_id:
    """
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        # Если жанр не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return genre


@router.get('', response_model=Page[Genre])
@cache(expire=3600)
async def genres_list(request: Request, genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    """
    Параметры поиска:
    - from: int начиная с какого элемента начинаем показ выдачи
    - size: int количество элементов в выдаче
    - query: str поисковая строка
    """
    # Формируем из параметров запроса словарь.
    search_params = dict(request.query_params.multi_items())

    # Формируем перечень полей, в которых будет происхождитть поиск, с весами
    search_fields = {'name': 3}
    genres = await genre_service.get_all(search_params=search_params, search_fields=search_fields)
    return paginate(genres)


add_pagination(router)
