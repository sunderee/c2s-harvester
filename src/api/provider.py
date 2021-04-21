from typing import Dict, Any
from aiohttp import ClientSession, ClientResponse
from ujson import dumps

from src.api.exceptions.api import ApiException


class ApiProvider:
    def __init__(self, base_url: str):
        self.__base_url: str = base_url

    async def get_request(self, endpoint: str, query_params: Dict[str, str]) -> str:
        async with ClientSession() as session:
            response: ClientResponse = await session.get(f'https://{self.__base_url}/{endpoint}', params=query_params)
            if response.status == 200:
                return await response.text('utf-8')
            raise ApiException([str(response.status), response.text()])

    async def post_request(self, endpoint: str, payload: Dict[str, Any]) -> str:
        async with ClientSession(json_serialize=dumps) as session:
            response: ClientResponse = await session.post(f'https://{self.__base_url}/{endpoint}', json=payload)
            if response.status == 200:
                return await response.text('utf-8')
            raise ApiException([str(response.status), response.text()])
