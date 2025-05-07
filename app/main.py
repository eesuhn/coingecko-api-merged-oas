from .oas_merger import OASMerger
from .endpoint_selector import EndpointSelector


class Main:
    def __init__(self) -> None:
        oas_merger = OASMerger()
        oas_merger.run()
        selector = EndpointSelector()
        selector.run()
