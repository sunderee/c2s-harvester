from typing import Union, List


class ApiException(Exception):
    def __init__(self, info: Union[str, List[str]]):
        self.__message: str = ','.join(info) if isinstance(info, list) else info
        super().__init__(self.__message)

    def __str__(self) -> str:
        return self.__message
