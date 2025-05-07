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
            "options",
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
        option_handlers = {
            "merge": OASMerger,
            "select": EndpointSelector
        }
        for option in self.args.options:
            handler = option_handlers.get(option)
            if handler:
                handler().run()
