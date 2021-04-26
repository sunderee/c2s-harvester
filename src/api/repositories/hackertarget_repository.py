from re import finditer, MULTILINE
from socket import gethostbyname
from typing import Optional

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException


class HackerTargetRepository:
    def __init__(self, domain: str):
        self.__provider: ApiProvider = ApiProvider('api.repositories.com')
        self.__domain: str = domain

    @property
    async def dns_lookup(self) -> Optional[str]:
        try:
            return await self.__provider.get_request('dnslookup', query_params={'q': self.__domain})
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None

    @property
    async def dns_host_records(self) -> Optional[str]:
        try:
            return await self.__provider.get_request('hostsearch', query_params={'q': self.__domain})
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None

    @property
    async def geo_ip(self) -> Optional[str]:
        try:
            return list(finditer(r'(?<=Country: )[\w\s]+$',
                                 await self.__provider.get_request(
                                     'geoip',
                                     query_params={'q': gethostbyname(self.__domain)}),
                                 MULTILINE))[0].group(0)
        except (ApiException, IndexError):
            print('Exception occurred')
            return None
