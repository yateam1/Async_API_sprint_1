from collections import defaultdict
from typing import Optional, List, Union
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions

from core.config import SAMPLE_SIZE
from models.films import Film
from models.persons import Person
from models.genres import Genre

ITEM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # Выставляем время жизни кеша — 5 минут


class ItemService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str):
        self.redis = redis
        self.elastic = elastic
        self.index = index

    # get_by_id возвращает объект фильма, персоны или жанра. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, item_id: UUID) -> Union[Film, Person, Genre]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        item = await self._item_from_cache(item_id)
        if not item:
            # Если объекта нет в кеше, то ищем его в Elasticsearch
            item = await self._get_item_from_elastic(item_id)
            if not item:
                # Если он отсутствует в Elasticsearch, значит, объекта вообще нет в базе
                return None
            # Сохраняем объект в кеш
            await self._put_item_to_cache(item)

        return item

    async def _get_item_from_elastic(self, item_id: UUID) -> Union[Film, Person, Genre]:
        try:
            doc = await self.elastic.get(self.index, item_id)
        except exceptions.NotFoundError:
            return None
        return doc

    async def _item_from_cache(self, item_id: UUID) -> Union[Film, Person, Genre]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(str(item_id))
        return data

    async def _put_item_to_cache(self, item: Union[Film, Person, Genre]):
        await self.redis.set(str(item.id), item.json(), expire=ITEM_CACHE_EXPIRE_IN_SECONDS)

    async def get_all(self, search_params: Optional[dict]) -> Union[List[Film], List[Person], List[Genre]]:
        body = defaultdict(lambda: defaultdict(dict))
        if search_params:
            body['query']['bool']['should'] = []
            for k, v in search_params.items():
                match_exp = defaultdict(lambda: defaultdict(dict))
                match_exp['match'][k] = v
                body['query']['bool']['should'].append(match_exp)
        else:
            body['query']['match_all'] = {}
        body['stored_fields'] = ['_id']
        data = await self.elastic.search(
            index=self.index,
            body=body,
            size=SAMPLE_SIZE
        )
        out = [await self.get_by_id(doc['_id']) for doc in data.get('hits').get('hits')]
        return out
