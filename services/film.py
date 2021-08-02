from functools import lru_cache
from typing import Optional, List
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import Depends

from core.config import SAMPLE_SIZE
from db.elastic import get_elastic
from db.redis import get_redis
from models.films import Film

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # Выставляем время жизни кеша — 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: UUID) -> Optional[Film]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм  в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: UUID) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except exceptions.NotFoundError:
            return None
        return Film(
            id=doc['_id'],
            **doc['_source'],
        )

    async def _film_from_cache(self, film_id: UUID) -> Optional[Film]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(str(film_id))
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film = Film.parse_raw(data)
        film.id = film.id  # Восстанавливаю тип айдишника записи
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(str(film.id), film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_all(self) -> List[Film]:
        data = await self.elastic.search(
            index='movies',
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
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
