from collections import namedtuple
from os import getcwd
from os.path import abspath
from typing import Dict, Optional

from dotenv import dotenv_values
from shodan import Shodan

ShodanResponse = namedtuple('ShodanResponse', 'domains hostnames org location vulnerabilities ports')


class ShodanRepository:
    def __init__(self):
        env_file: Dict[str, Optional[str]] = dotenv_values(dotenv_path=f'{abspath(getcwd())}/.env')
        self.__shodan = Shodan(env_file["SHODAN"])

    def search(self, ip_address: str):
        res = dict(self.__shodan.host(ip_address, minify=True))
        return ShodanResponse(
            domains=res['domains'],
            hostnames=res['hostnames'],
            org=res['org'],
            location=f'{res["country_code"]}, {res["city"]} ({res["latitude"]}, {res["longitude"]})',
            vulnerabilities=res['vulns'],
            ports=res["ports"])
