from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, add_pagination, paginate

from models import Film
from services.film import FilmService, get_film_service
from utils.url_misc import get_params

router = APIRouter()


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=Film)
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
async def movies_list(request: Request, film_service: FilmService = Depends(get_film_service)) -> List[Film]:
    """
    Предоставляет информацию о всех фильмах
    Можно указать параметры поиска:
    - title: str
    - description: str
    """
    # Формируем из параметров запроса словарь.
    search_params = get_params(request)
    films = await film_service.get_all(search_params)
    return paginate(films)

add_pagination(router)
