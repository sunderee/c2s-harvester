from argparse import ArgumentParser, Namespace
from asyncio import run
from socket import gethostbyname
from typing import Optional, List, Tuple

from dotenv import load_dotenv

from src.api.repositories.bing_repository import BingRepository, BingResult
from src.api.repositories.censys_repository import CensysRepository
from src.api.repositories.certspotter_repository import CertSpotterRepository, CertSpotterResponse
from src.api.repositories.hackertarget_repository import HackerTargetRepository
from src.api.repositories.hunter_repository import HunterRepository, HunterResponse
from src.api.repositories.otx_repository import OTXRepository
from src.api.repositories.shodan_repository import ShodanRepository, ShodanResponse

load_dotenv()
bing = BingRepository()
censys = CensysRepository()
cert_spotter = CertSpotterRepository()
hacker_target = HackerTargetRepository()
hunter = HunterRepository()
otx = OTXRepository()
shodan = ShodanRepository()


def parse_arguments() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('domain', help='Domain you are trying to enumerate and test')
    parser.add_argument(
        '-f', '--file',
        action='store', dest='file',
        help='Where you wanna store the outputs, if not specified you will get results printed to stdout')
    return parser.parse_args()


async def main():
    arguments: Namespace = parse_arguments()
    domain: str = str(arguments.domain)
    if len(domain) == 0:
        print('Cannot have empty domain!')
        exit(1)

    ip_address: str = gethostbyname(domain)

    bing_results: Optional[BingResult] = await bing.search(domain)
    censys_results: Optional[dict] = await censys.query_ip(ip_address)
    cert_spotter_results: Optional[List[CertSpotterResponse]] = await cert_spotter.retrieve_certificate_info(domain)
    hacker_target_results: Tuple[Optional[str], Optional[str], Optional[str]] = (
        await hacker_target.dns_lookup(domain),
        await hacker_target.dns_host_records(domain),
        await hacker_target.geo_ip(domain)
    )
    hunter_results: Optional[List[HunterResponse]] = await hunter.domain_lookup(domain)
    otx_results: Optional[List[str]] = await otx.passive_dns(domain)
    shodan_results: ShodanResponse = shodan.search(ip_address)

    outputs: str = 'ENUMERATION RESULTS\n' + \
                   f'BING RESULTS\n{bing_results}\n\n' + \
                   f'CENSYS RESULTS\n{censys_results}\n\n' + \
                   f'CERT SPOTTER RESULTS\n{cert_spotter_results}' + \
                   f'HACKERTARGET API RESULTS\n{hacker_target_results}' + \
                   f'HUNTER RESULTS\n{hunter_results}' + \
                   f'OTX RESULTS\n{otx_results}' + \
                   f'SHODAN RESULTS\n{shodan_results}'

    if arguments.file is not None:
        with open(str(arguments.file), 'w') as file:
            file.write(outputs)
        exit(1)
    print(outputs)


if __name__ == '__main__':
    run(main())
