from http import HTTPStatus
from typing import List, Optional
from fastapi_cache.decorator import cache

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi_pagination import Page, add_pagination, paginate

from models import Person
from services.person import PersonService, get_person_service

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
async def persons_list(request: Request, person_service: PersonService = Depends(get_person_service),
                      from_: Optional[int] = Query(0, title='Пагинация "c"', alias='from'),
                      size_: Optional[int] = Query(10, title='Пагинация "cколько"', alias='size'),
                      query_: Optional[str] = Query(None, title='Поисковая строка', alias='query')) -> List[Person]:
    """
    Предоставляет информацию о всех персонах
    Параметры поиска:
    - from: int начиная с какого элемента начинаем показ выдачи
    - size: int количество элементов в выдаче
    - query: str поисковая строка
    """
    # Формируем из параметров запроса словарь.
    search_params = {'from': from_, 'size': size_, 'query': query_}

    # Формируем перечень полей, в которых будет происхождитть поиск, с весами
    search_fields = {'last_name': 5, 'first_name': 3}
    persons = await person_service.get_all(search_params=search_params, search_fields=search_fields)
    return paginate(persons)


add_pagination(router)
