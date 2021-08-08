from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Union
from uuid import UUID

import backoff
from elasticsearch import AsyncElasticsearch, exceptions
from pydantic import parse_obj_as

from models import Film, Person, Genre


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

    @backoff.on_exception(backoff.expo,
                          (exceptions.ConnectionError, ),
                          max_time=10)
    async def get_by_id(self, item_id: UUID) -> Optional[Union[Film, Person, Genre]]:
        try:
            doc = await self.elastic.get(self.elastic_index_name, item_id)
        except exceptions.NotFoundError:
            return
        return self.model(id=doc['_id'], **doc['_source'])

    @backoff.on_exception(backoff.expo,
                          (exceptions.ConnectionError, ),
                          max_time=10)
    async def get_all(self, search_params: Optional[dict],
                      search_fields: Optional[dict]) -> Union[list[Film], list[Person], list[Genre]]:
        """
        Получение записей по поисковой строке
        """

        body = defaultdict(lambda: defaultdict(dict))
        body['from'] = search_params['from']
        body['size'] = search_params['size']

        if search_params['query']:
            
            body['query']['bool']['should'] = []
            for field, weight in search_fields.items():
                match = defaultdict(lambda: defaultdict(dict))
                match['match'][field]['query'] = search_params['query']
                match['match'][field]['boost'] = weight
                body['query']['bool']['should'].append(match)

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
