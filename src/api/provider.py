from typing import Dict, Any, Optional, Union
from aiohttp import ClientSession, ClientResponse
from ujson import dumps

from src.exceptions.api import ApiException


class ApiProvider:
    def __init__(self, base_url: str):
        self.__base_url: str = base_url

    async def get_request(
            self,
            endpoint: str,
            query_params: Optional[Dict[str, Union[str, int, Any]]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> str:
        async with ClientSession(headers=headers) as session:
            response: ClientResponse = await session.get(f'https://{self.__base_url}/{endpoint}', params=query_params)
            if response.status == 200:
                return await response.text('utf-8')
            raise ApiException([str(response.status), await response.text('utf-8')])

    async def post_request(
            self,
            endpoint: str,
            payload: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> str:
        async with ClientSession(json_serialize=dumps, headers=headers) as session:
            response: ClientResponse = await session.post(f'https://{self.__base_url}/{endpoint}', json=payload)
            if response.status == 200:
                return await response.text('utf-8')
            raise ApiException([str(response.status), await response.text()])
