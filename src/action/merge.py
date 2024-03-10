#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


def install_toml() -> None:
    """pip install toml"""
    command = f"{sys.executable} -m pip install toml"
    subprocess.run(shlex.split(command), check=True)  # noqa: S603


def load_toml(path: str | Path) -> dict[str, Any] | None:
    """toml to dict or null"""
    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()

    if not path.exists():
        return None

    with path.open("rb") as file:
        return tomllib.load(file)


def merge_toml(*datas: dict[str, Any]) -> dict[str, Any]:
    """merge toml dicts"""
    result: dict[str, Any] = {"sources": []}

    for data in datas:
        value = data.copy()
        source = value.pop("sources", None)

        result.update(value)
        if not source or not isinstance(source, list):
            continue

        names = {x["name"] for x in source}
        origin_source = [x for x in result["sources"] if x["name"] not in names]

        result["sources"] = [*origin_source, *source]

    return result


def dump_toml(path: str | Path, data: dict[str, Any]) -> None:
    """dict to toml"""
    import toml  # pyright: ignore[reportMissingModuleSource]

    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()

    with path.open("w+") as file:
        toml.dump(data, file)


def main(file: str | Path, *files: str | Path) -> None:  # noqa: D103
    data = load_toml(file)
    if data is None:
        raise FileNotFoundError(file)

    tomls = [value for file in files if (value := load_toml(file)) is not None]

    if not tomls:
        return

    result = merge_toml(data, *tomls)

    install_toml()
    dump_toml(file, result)


if __name__ == "__main__":
    main(*sys.argv[1:])
