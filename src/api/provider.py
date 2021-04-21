from typing import Dict, Optional, Any, Coroutine
from aiohttp import ClientSession
from ujson import dumps


class ApiProvider:
    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def get_request(self, endpoint: str, query_params: Dict[str, str]) -> Coroutine[Optional[str]]:
        async with ClientSession() as session:
            async with session.get(f'https://{self.__base_url}/{endpoint}', params=query_params) as response:
                return response.text('utf-8') if response.status == 200 else None

    async def post_request(self, endpoint: str, payload: Dict[str, Any]) -> Coroutine[Optional[str]]:
        async with ClientSession(json_serialize=dumps) as session:
            async with session.post(f'https://{self.__base_url}/{endpoint}', json=payload) as response:
                return response.text('utf-8') if response.status == 200 else None
