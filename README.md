# C2S Harvester

*C2S Harvester* is a "fork" of [theHarvester](https://github.com/laramies/theHarvester) tool, but instead of having 10+
options, it runs pre-defined passive and active recon tasks. Project is still heavily based on `theHarvester`, list of
resources copied from it can be found below.

Aside from `theHarvester`, this tool takes inspiration from [AutoSploit](https://github.com/NullArray/AutoSploit) and
[Infection Monkey](https://github.com/guardicore/monkey). Source code comments evidently document where certain sections
were taken from.

I would like to thank everyone involved in creation of aforementioned tools.

## Usage

Make sure you have [`nmap`](https://nmap.org) installed on your system. Create a `.env` file at the project root with
the API keys to third-party providers:

```dotenv
BING=XXX
CENSYS=XXX
GITHUB=XXX
HUNTER=XXX
INTELX=XXX
PENTEST_TOOLS=XXX
PROJECT_DISCOVERY=XXX
SECURITY_TRAILS=XXX
SHODAN=XXX
SPYSE="XXX
```

### Installation

The easiest way to get `C2S Harvester` up and running is by using Docker. The alternative option is creating a virtual
environment, installing dependencies, running setup tasks and executing the program. Both options yield same results, but
containerized approach is recommended (easier to use).

### What does it do?

Similarly to `theHarvester`, it runs a series of passive and active recon tasks. Alongside with that, it also attempts
to exploit found vulnerabilities through series of tasks. The vulnerability analysis and exploitation is **not** a reliable
tool, but it's included because it might help identify possible points of attack faster.

## License

Project is licensed under MIT license.