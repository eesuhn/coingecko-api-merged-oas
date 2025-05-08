import argparse

from .oas_merger import OASMerger
from .endpoint_selector import EndpointSelector

DESIRED_PATHS = [
    "/ping",
    "/coins/list"
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
