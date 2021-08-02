from functools import lru_cache
from typing import Optional, List
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from core.config import SAMPLE_SIZE
from db.elastic import get_elastic
from db.redis import get_redis
from models.genres import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # Выставляем время жизни кеша — 5 минут


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: UUID) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except exceptions.NotFoundError:
            return None
        return Genre(id=genre_id, name=doc['_source']['name'])

    async def _genre_from_cache(self, genre_id: UUID) -> Optional[Genre]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(str(genre_id))
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        # Сохраняем данные о фильме, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(str(genre.id), genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)

    async def _get_all(self) -> List[Genre]:
        data = await self.elastic.search(
            index='genres',
            body={
                "query": {
                    "match_all": {}
                },
                'stored_fields': []
            },
            size = SAMPLE_SIZE
        )
        out = [await self.get_by_id(doc['_id']) for doc in data.get('hits').get('hits')]
        return out


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
