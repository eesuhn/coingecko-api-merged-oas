import argparse

from .oas_merger import OASMerger
from .endpoint_selector import EndpointSelector

DESIRED_PATHS = [
    # General
    "/key",  # 💼 API Usage
    "/simple/price",  # Coin Price by IDs and Symbols
    "/simple/token_price/{id}",  # Coin Price by Token Addresses
    "/coins/list",  # Coins List (ID Map)
    "/coins/{id}",  # Coin Data by ID
    "/coins/{id}/market_chart/range",  # Coin Historical Chart Data within Time Range by ID
    "/coins/{id}/ohlc/range",  # 💼 Coin OHLC Chart within Time Range by ID
    "/coins/categories",  # Coins Categories List with Market Data

    # Onchain
    "/onchain/simple/networks/{network}/token_price/{addresses}",  # Token Price by Token Addresses
    "/onchain/networks",  # Supported Networks List (ID Map)
    "/onchain/networks/{network}/trending_pools",  # Trending Pools by Network
    "/onchain/networks/{network}/pools/multi/{addresses}",  # Multiple Pools Data by Pool Addresses
    "/onchain/networks/{network}/pools",  # Top Pools by Network
    "/onchain/pools/megafilter",  # 🔥 Megafilter for Pools
    "/onchain/networks/{network}/tokens/multi/{addresses}"  # Tokens Data by Token Addresses
]


class Main:
    def __init__(self) -> None:
        self.parse_args()
        self.parse_options()

    def parse_args(self) -> None:
        args_parser = argparse.ArgumentParser(
            description="Merge CoinGecko OAS"
        )
        args_parser.add_argument(
            dest="options",
            type=str,
            nargs="+",
            choices=[
                "merge",
                "select"
            ],
            help="Option(s) to run",
        )
        self.args = args_parser.parse_args()

    def parse_options(self) -> None:
        oas_merger = OASMerger()
        endpoint_selector = EndpointSelector(
            paths_to_select=DESIRED_PATHS
        )
        option_handlers = {
            "merge": oas_merger,
            "select": endpoint_selector
        }
        for option in self.args.options:
            if option in option_handlers:
                option_handlers[option].run()
