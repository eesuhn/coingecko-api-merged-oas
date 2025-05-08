import sys
import json

from pathlib import Path
from typing import Optional
from colorama import Fore


class RootPath:
    @staticmethod
    def get_root() -> Path:
        """Get the root directory of the project."""
        return Path(__file__).parent.parent

    @staticmethod
    def get_package_root() -> Path:
        """Get the root directory of the package."""
        return Path(__file__).parent

    @staticmethod
    def get_venv_root() -> Path:
        """Get the root directory of the virtual environment."""
        return Path(sys.executable).parent


class JsonFile:
    @staticmethod
    def read_json(
        file_path: Path,
        root: Path = RootPath.get_package_root()
    ) -> dict:
        full_path = (root / file_path).with_suffix(".json")
        with open(
            file=full_path,
            mode="r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    @staticmethod
    def write_json(
        data: Optional[dict],
        file_path: Path,
        root: Path = RootPath.get_package_root(),
        indent: int = 2,
        sort_keys: bool = False
    ) -> bool:
        if data is None:
            return False
        full_path = (root / file_path).with_suffix(".json")
        with open(
            file=full_path,
            mode="w",
            encoding="utf-8"
        ) as f:
            json.dump(
                obj=data,
                fp=f,
                indent=indent,
                sort_keys=sort_keys
            )
        return True

    @staticmethod
    def print_json(
        json_data: Optional[dict],
        indent: int = 2,
        sort_keys: bool = False
    ) -> None:
        if json_data is None:
            pass
        print(
            json.dumps(
                obj=json_data,
                indent=indent,
                sort_keys=sort_keys
            )
        )


class ColorPrint:
    @staticmethod
    def print_color(
        m: str,
        prefix: str = "placeholder",
        color: str = Fore.RESET
    ) -> None:
        print(f"[{color}{prefix}{Fore.RESET}] {m}")

    @staticmethod
    def print_success(
        m: str,
        prefix: str = "success"
    ) -> None:
        ColorPrint.print_color(m, prefix, Fore.GREEN)

    @staticmethod
    def print_warning(
        m: str,
        prefix: str = "warning"
    ) -> None:
        ColorPrint.print_color(m, prefix, Fore.YELLOW)

    @staticmethod
    def print_error(
        m: str,
        prefix: str = "error"
    ) -> None:
        ColorPrint.print_color(m, prefix, Fore.RED)

    @staticmethod
    def print_info(
        m: str,
        prefix: str = "info"
    ) -> None:
        ColorPrint.print_color(m, prefix, Fore.MAGENTA)
