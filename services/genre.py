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
from services.base import ItemService


class GenreService(ItemService):
    async def _get_item_from_elastic(self, item_id: UUID) -> Optional[Genre]:
        doc = await super()._get_item_from_elastic(item_id)
        return Genre(
            id=doc['_id'],
            **doc['_source'],
        )
    
    async def _item_from_cache(self, item_id: UUID) -> Optional[Genre]:
        data = await super()._item_from_cache(item_id)
        # pydantic предоставляет удобное API для создания объекта моделей из json
        if not data:
            return None
        item = Genre.parse_raw(data)
        return item


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic, index='genres')
