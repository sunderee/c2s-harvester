from collections import namedtuple
from os import getcwd
from os.path import abspath
from typing import Optional, Dict, Union, Any, List, Iterator

from dotenv import dotenv_values
from ujson import loads

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException

BingResult = namedtuple('BingResult', 'matches values')


class BingRepository:
    def __init__(self):
        self.__provider: ApiProvider = ApiProvider('api.bing.microsoft.com')
        self.__bing_api: Optional[str] = dotenv_values(dotenv_path=f'{abspath(getcwd())}/.env')['BING']

    async def search(self, query: str) -> Optional[BingResult]:
        try:
            raw_result: str = await self.__provider.get_request(
                'v7.0/search',
                query_params={'q': query, 'count': 50, 'responseFilter': 'entities,webpages', 'safeSearch': 'off'},
                headers={'Ocp-Apim-Subscription-Key': self.__bing_api or ''}
            )
            result: Union[Dict[str, Any], List[Dict[str, Any]]] = loads(raw_result)
            raw_values: Iterator[Dict[str, Any]] = map(
                lambda element: {'title': element['name'], 'description': element['snippet'], 'url': element['url']},
                list(result['webPages']['value'])
            )
            return BingResult(matches=result['webPages']['totalEstimatedMatches'], values=list(raw_values))
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None
