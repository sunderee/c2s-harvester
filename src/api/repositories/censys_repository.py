from base64 import b64encode
from os import getcwd
from os.path import abspath
from typing import Optional, Dict

from dotenv import dotenv_values
from ujson import loads

from src.api.provider import ApiProvider
from src.exceptions.api import ApiException


class CensysRepository:
    def __init__(self):
        self.__provider = ApiProvider('censys.io')
        env_file: Dict[str, Optional[str]] = dotenv_values(dotenv_path=f'{abspath(getcwd())}/.env')
        self.__credentials: str = b64encode(f'{env_file["CENSYS_ID"]}:{env_file["CENSYS_SECRET"]}'.encode()).decode()

    async def query_ip(self, ip_address: str) -> Optional[dict]:
        try:
            result: str = await self.__provider.get_request(
                f'api/v1/view/ipv4/{ip_address}',
                headers={'Authorization': f'Basic {self.__credentials}'})
            return loads(result)
        except ApiException as exception:
            print(f'Exception occurred:\n{exception}')
            return None
