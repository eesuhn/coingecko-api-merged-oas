import argparse

from .oas_merger import OASMerger
from .endpoint_selector import EndpointSelector


class Main:
    def __init__(self) -> None:
        self.parse_args()
        self.parse_options()

    def parse_args(self) -> None:
        args_parser = argparse.ArgumentParser(
            description="Merge CoinGecko OAS"
        )
        args_parser.add_argument(
            "-NO", "--non-onchain",
            dest="non_onchain_count",
            type=int,
            default=10,
            help="Number of non-onchain endpoints to select",
        )
        args_parser.add_argument(
            "-O", "--onchain",
            dest="onchain_count",
            type=int,
            default=5,
            help="Number of onchain endpoints to select",
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
            non_onchain_count=self.args.non_onchain_count,
            onchain_count=self.args.onchain_count
        )
        option_handlers = {
            "merge": oas_merger,
            "select": endpoint_selector
        }
        for option in self.args.options:
            if option in option_handlers:
                option_handlers[option].run()
