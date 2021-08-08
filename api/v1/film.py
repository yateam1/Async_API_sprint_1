from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_cache.decorator import cache

from models import Film
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/{film_id}', response_model=Film)
@cache(expire=3600)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    """
    Предоставляет информацию о кинопроизведении по его id
    :param film_id:
    """
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return film


@router.get('', response_model=Page[Film])
@cache(expire=3600)
async def movies_list(film_service: FilmService = Depends(get_film_service),
                      from_: Optional[int] = Query(0, title='Пагинация "c"', alias='from'),
                      size_: Optional[int] = Query(10, title='Пагинация "cколько"', alias='size'),
                      query_: Optional[str] = Query(None, title='Поисковая строка', alias='query')) -> List[Film]:
    """
    Предоставляет информацию о фильмах
    Параметры поиска:
    - from: int начиная с какого элемента начинаем показ выдачи
    - size: int количество элементов в выдаче
    - query: str поисковая строка
    """
    
    search_params = {'from': from_, 'size': size_, 'query': query_}

    # Формируем перечень полей, в которых будет происхождитть поиск, с весами
    search_fields = {'title': 5, 'actors': 3, 'description': 1}

    films = await film_service.get_all(search_params=search_params, search_fields=search_fields)
    return paginate(films)

add_pagination(router)
