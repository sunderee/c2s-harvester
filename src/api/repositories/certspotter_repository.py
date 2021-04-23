from collections import namedtuple
from typing import Union, Dict, Any, List, Optional

from ujson import loads

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException

CertSpotterResponse = namedtuple('CertSpotterResponse', 'tbs_certificate dns_names public_key')


class CertSpotterRepository:
    def __init__(self):
        self.__provider = ApiProvider('api.certspotter.com')

    async def retrieve_certificate_info(self, domain: str) -> Optional[List[CertSpotterResponse]]:
        try:
            raw_result: str = await self.__provider.get_request(
                'v1/issuances',
                query_params={'domain': domain, 'expand': 'dns_names'})
            result: Union[Dict[str, Any], List[Dict[str, Any]]] = loads(raw_result)
            return list(map(lambda element: CertSpotterResponse(
                tbs_certificate=element['tbs_sha256'],
                dns_names=element['dns_names'],
                public_key=element['pubkey_sha256']
            ), result))
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None
