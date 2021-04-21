from re import finditer, MULTILINE
from socket import gethostbyname

from src.api.provider import ApiProvider


class HackerTargetRepository:
    def __init__(self, domain: str):
        self.__provider: ApiProvider = ApiProvider('api.hackertarget.com')
        self.__domain: str = domain

    @property
    async def dns_lookup(self) -> str:
        return await self.__provider.get_request('dnslookup', {'q': self.__domain})

    @property
    async def dns_host_records(self) -> str:
        return await self.__provider.get_request('hostsearch', {'q': self.__domain})

    @property
    async def geo_ip(self) -> str:
        return list(finditer(
            r'(?<=Country: )[\w\s]+$',
            await self.__provider.get_request('geoip', {'q': gethostbyname(self.__domain)}),
            MULTILINE
        ))[0].group(0)
