import json
import sys

from colorama import Back
from typing import Optional
from pathlib import Path


def get_root() -> Path:
    return Path(__file__).parent.parent


def get_package_root() -> Path:
    return Path(__file__).parent


def get_venv_root() -> Path:
    return Path(sys.executable).parent


def load_json(
    filename: str,
    root: Path = get_package_root()
) -> dict:
    with open(
        root / f"{filename}.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(
    data: Optional[dict],
    filename: str,
    root: Path = get_package_root()
) -> None:
    if data is None:
        return
    with open(
        root / f"{filename}.json",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(data, indent=2)
        )


def print_info(
    m: str
) -> None:
    print(f"{Back.MAGENTA}INFO{Back.RESET} {m}")


def print_success(
    m: str
) -> None:
    print(f"{Back.GREEN}SUCCESS{Back.RESET} {m}")
