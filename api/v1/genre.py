from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import BaseModel

from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


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

    return genre


@router.get('', response_model=Page[Genre])
async def genres_list(genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    """
    Предоставляет информацию о всех жанрах
    """
    genres = await genre_service._get_all()
    return paginate(genres)


add_pagination(router)