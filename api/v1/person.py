from http import HTTPStatus
from typing import List
from fastapi_cache.decorator import cache

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_pagination import Page, add_pagination, paginate

from models import Person
from services.person import PersonService, get_person_service
from utils.url_misc import get_params

router = APIRouter()


# Внедряем PersonService с помощью Depends(get_person_service)
@router.get('/{person_id}', response_model=Person)
@cache(expire=3600)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    """
    Предоставляет информацию о персоне по её id
    :param person_id:
    """
    person= await person_service.get_by_id(person_id)
    if not person:
        # Если жанр не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return person


@router.get('', response_model=Page[Person])
@cache(expire=3600)
async def persons_list(request: Request, person_service: PersonService = Depends(get_person_service)) -> List[Person]:
    """
    Предоставляет информацию о всех персонах
    Можно указать параметры поиска:
    - first_name: str
    - last_name: str
    """
    search_params = get_params(request)
    persons = await person_service.get_all(search_params)
    return paginate(persons)


add_pagination(router)
