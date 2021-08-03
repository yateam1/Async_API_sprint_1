from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, List, Union
from uuid import UUID

from elasticsearch import AsyncElasticsearch, exceptions

from core.config import SAMPLE_SIZE
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

    async def get_by_id(self, item_id: UUID) -> Optional[Union[Film, Person, Genre]]:
        try:
            doc = await self.elastic.get(self.elastic_index_name, item_id)
        except exceptions.NotFoundError:
            return
        return self.model(id=doc['_id'], **doc['_source'])

    async def get_all(self, search_params: Optional[dict]) -> List[Union[Film, Person, Genre]]:
        body = defaultdict(lambda: defaultdict(dict))
        if search_params:
            body['query']['bool']['should'] = []
            for k, v in search_params.items():
                match_exp = defaultdict(lambda: defaultdict(dict))
                match_exp['match'][k] = v
                body['query']['bool']['should'].append(match_exp)
        else:
            body['query']['match_all'] = {}
        body['stored_fields'] = {}
        data = await self.elastic.search(
            index=self.elastic_index_name,
            body=body,
            size=SAMPLE_SIZE
        )
        return data.get('hits', {}).get('hits', [])
