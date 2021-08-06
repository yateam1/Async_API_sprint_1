from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from models import Person
from services.base import ItemService


class PersonService(ItemService):
    elastic_index_name = 'persons'
    model = Person


def get_person_service(elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(elastic)
