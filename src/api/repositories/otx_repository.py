from typing import Optional, List

from ujson import loads

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException


class OTXRepository:
    def __init__(self):
        self.__provider: ApiProvider = ApiProvider('otx.alienvault.com')

    async def passive_dns(self, domain: str) -> Optional[List[str]]:
        try:
            raw_response = await self.__provider.get_request(f'api/v1/indicators/domain/{domain}/passive_dns')
            return list(map(
                lambda e: f'{e["record_type"]}: {e["address"]},{e["hostname"]},{e["asn"]}',
                list(dict(loads(raw_response))['passive_dns'])))
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None
