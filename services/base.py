from abc import ABC, abstractmethod
from collections import defaultdict
from http import HTTPStatus
from typing import Optional, Union
from uuid import UUID

from elasticsearch import AsyncElasticsearch, exceptions
from fastapi import HTTPException
from pydantic import parse_obj_as, ValidationError

from models import Film, Person, Genre
from services.api_params import APIParams


class ItemService(ABC):

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    @property
    @abstractmethod
    def elastic_index_name(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def model(*args, **kwargs) -> Union[Film, Person, Genre]:
        pass

    async def get_by_id(self, item_id: UUID) -> Optional[Union[Film, Person, Genre]]:
        try:
            doc = await self.elastic.get(self.elastic_index_name, item_id)
        except exceptions.NotFoundError:
            return
        return self.model(id=doc['_id'], **doc['_source'])

    async def get_all(self, search_params: Optional[dict],
                      search_fields: Optional[dict]) -> Union[list[Film], list[Person], list[Genre]]:
        """
        Получение записей по поисковой строке
        """

        try:
            search_params = APIParams(**search_params)
        except ValidationError as err:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=err)
        from_ = search_params.from_
        size_ = search_params.size_
        query_ = search_params.query_
        body = defaultdict(lambda: defaultdict(dict))
        body['from'] = from_
        body['size'] = size_

        if query_:
            for field, weight in search_fields.items():
                body['search_fields'][k]['weight'] = weight
            body['query'] = query_

        else:
            body['query']['match_all'] = {}

        data = await self.elastic.search(
            index=self.elastic_index_name,
            body=body
        )
        items = map(
            lambda item: {'id': item['_id'], **item['_source']},
            data.get('hits', {}).get('hits', [])
        )
        
        return parse_obj_as(list[self.model], list(items))
