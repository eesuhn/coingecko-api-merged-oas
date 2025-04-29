from .oas_merger import OASMerger


class Main:
    def __init__(self) -> None:
        self.oas_merger = OASMerger()
        self.oas_merger.run()
