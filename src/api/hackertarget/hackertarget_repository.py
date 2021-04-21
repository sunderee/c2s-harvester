from re import finditer, MULTILINE
from socket import gethostbyname
from typing import Coroutine

from src.api.exceptions.api import ApiException
from src.api.provider import ApiProvider


class HackerTargetRepository:
    def __init__(self, domain: str):
        self.__provider: ApiProvider = ApiProvider('api.hackertarget.com')
        self.__domain: str = domain

    async def dns_lookup(self) -> Coroutine[str]:
        result = await self.__provider.get_request('dnslookup', {'q': self.__domain})
        if result is not None:
            return result
        raise ApiException('DNS lookup failed')

    async def dns_host_records(self) -> Coroutine[str]:
        result = await self.__provider.get_request('hostsearch', {'q': self.__domain})
        if result is not None:
            return result
        raise ApiException('DNS host records (subdomains) lookup failed')

    async def geo_ip(self):
        result = await self.__provider.get_request('geoip', {'q': gethostbyname(self.__domain)})
        if result is not None:
            regex = r'(?<=Country: )[\w\s]+$'
            assert isinstance(result, str)
            return list(finditer(regex, result, MULTILINE))[0].group(0)
        raise ApiException(['Geolocation of IP failed', result])
