from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from db.elastic import get_elastic
from models.genres import Genre
from services.base import ItemService


class GenreService(ItemService):
    elastic_index_name = 'genres'
    model = Genre


def get_genre_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> GenreService:
    return GenreService(elastic)
