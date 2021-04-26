from collections import namedtuple
from os import getcwd
from os.path import abspath
from typing import Dict, Optional, List

from dotenv import dotenv_values
from ujson import loads

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException

HunterResponse = namedtuple('HunterResponse', 'value name linked_in twitter phone emails')


class HunterRepository:
    def __init__(self):
        self.__provider: ApiProvider = ApiProvider('api.hunter.io')
        env_file: Dict[str, Optional[str]] = dotenv_values(dotenv_path=f'{abspath(getcwd())}/.env')
        self.__api_key = env_file['HUNTER']

    async def domain_lookup(self, domain: str) -> Optional[List[HunterResponse]]:
        try:
            raw_result = await self.__provider.get_request(
                'v2/domain-search',
                {'domain': domain, 'api_key': self.__api_key or ''}
            )
            result: dict = loads(raw_result)
            return list(map(lambda element: HunterResponse(
                value=element['value'],
                name=f'{element["first_name"]} {element["last_name"]}',
                linked_in=element['linkedin'],
                twitter=element['twitter'],
                phone=element['phone_number'],
                emails=list(map(lambda data: data['url'], list(element['emails'])))
            ), list(result['data']['emails'])))
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None
