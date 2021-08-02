from functools import lru_cache
from typing import Optional, List
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.config import SAMPLE_SIZE
from db.elastic import get_elastic
from db.redis import get_redis
from models.persons import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # Выставляем время жизни кеша — 5 минут


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        person = await self._person_from_cache(str(person_id))
        if not person:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            person = await self._get_person_from_elastic(person_id)
            if not person:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: UUID) -> Optional[Person]:
        doc = await self.elastic.get('persons', person_id)
        return Person(
            id=doc['_id'],
            **doc['_source'],
        )

    async def _person_from_cache(self, person_id: UUID) -> Optional[Person]:
        data = await self.redis.get(str(person_id))
        if not data:
            return None

        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, person: Person):
        await self.redis.set(str(person.id), person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _get_all(self) -> List[Person]:
        data = await self.elastic.search(
            index='persons',
            body={
                "query": {
                    "match_all": {}
                },
                'stored_fields': []
            },
            size=SAMPLE_SIZE
        )
        out = [await self.get_by_id(doc['_id']) for doc in data.get('hits').get('hits')]
        return out


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
