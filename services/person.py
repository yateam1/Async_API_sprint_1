from functools import lru_cache
from typing import Optional
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.persons import Person
from services.base import ItemService


class PersonService(ItemService):
    async def _get_item_from_elastic(self, item_id: UUID) -> Optional[Person]:
        doc = await super()._get_item_from_elastic(item_id)
        return Person(
            id=doc['_id'],
            **doc['_source'],
        )
    
    async def _item_from_cache(self, item_id: UUID) -> Optional[Person]:
        data = await super()._item_from_cache(item_id)
        # pydantic предоставляет удобное API для создания объекта моделей из json
        if not data:
            return None
        item = Person.parse_raw(data)
        return item


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic, index='persons')
