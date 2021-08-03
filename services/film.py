from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from db.elastic import get_elastic
from models.films import Film
from services.base import ItemService


class FilmService(ItemService):
    elastic_index_name = 'movies'
    model = Film


def get_film_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> FilmService:
    return FilmService(elastic)
