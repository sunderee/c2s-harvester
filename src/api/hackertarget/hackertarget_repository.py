from asyncio import wait, get_event_loop, ALL_COMPLETED
from concurrent.futures import ThreadPoolExecutor
from re import finditer, MULTILINE
from socket import gethostbyname
from typing import Optional, Coroutine, Any

from src.api.exceptions.api import ApiException
from src.api.provider import ApiProvider


class HackerTargetRepository:
    def __init__(self, domain: str):
        self.__provider: ApiProvider = ApiProvider('api.hackertarget.com')
        self.__domain: str = domain

    async def dns_lookup(self) -> Coroutine[Any, Any, Optional[str]]:
        return await self.__provider.get_request('dnslookup', {'q': self.__domain})

    async def dns_host_records(self) -> Coroutine[Any, Any, Optional[str]]:
        return await self.__provider.get_request('hostsearch', {'q': self.__domain})

    async def geo_ip(self) -> str:
        result: Optional[str] = (await self.__provider.get_request(
            'geoip',
            {'q': gethostbyname(self.__domain)}
        )).cr_await
        if result is not None:
            regex = r'(?<=Country: )[\w\s]+$'
            return list(finditer(regex, result, MULTILINE))[0].group(0)
        raise ApiException(['Geolocation of IP failed', result])


repository = HackerTargetRepository('ipm.si')
loop = get_event_loop()
executor = ThreadPoolExecutor(max_workers=5)


async def non_blocking(l, e):
    await wait(
        fs={
            l.run_in_executor(e, repository.dns_host_records),
            l.run_in_executor(e, repository.dns_lookup),
            l.run_in_executor(e, repository.geo_ip)
        },
        return_when=ALL_COMPLETED
    )


loop.run_until_complete(non_blocking(loop, executor))
