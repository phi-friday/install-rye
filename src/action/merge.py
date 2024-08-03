#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger("install-rye.merge")
logger.addHandler(logging.StreamHandler(sys.stdout))

if os.getenv("IS_DEBUG", "0") == "1":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def check_toml() -> bool:
    """check toml"""
    command = f"{sys.executable} -m pip list"
    result = subprocess.run(  # noqa: S603
        shlex.split(command), check=True, capture_output=True, text=True
    )
    return "toml" in result.stdout


def check_pip() -> bool:
    """check pip"""
    command = f"{sys.executable} -m pip --version"
    result = subprocess.run(  # noqa: S603
        shlex.split(command), check=False, capture_output=True, text=True
    )
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        return False
    return True


def install_pip() -> None:
    """install pip"""
    command = f"{sys.executable} -m ensurepip --upgrade"
    subprocess.run(shlex.split(command), check=True)  # noqa: S603


def install_toml() -> None:
    """pip install toml"""
    command = f"{sys.executable} -m pip install --user toml"
    subprocess.run(shlex.split(command), check=True)  # noqa: S603


def load_toml(path: str | Path) -> dict[str, Any] | None:
    """toml to dict or null"""
    import toml  # pyright: ignore[reportMissingModuleSource]

    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()

    if not path.exists():
        logger.debug("there is no file: %s", path)
        return None

    with path.open("r") as file:
        result = toml.load(file)

    logger.debug("path: %s, data: %s", path, result)
    return result


def merge_toml(*datas: dict[str, Any]) -> dict[str, Any]:
    """merge toml dicts"""
    result: dict[str, Any] = {"sources": []}

    for data in datas:
        value = data.copy()
        source = value.pop("sources", None)

        for key, sub_value in value.items():
            if not isinstance(sub_value, dict):
                continue

            origin_value: dict[str, Any] = result.setdefault(key, {})
            origin_value.update(sub_value)

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
    all_files = {file, *files}
    if len(all_files) == 1:
        return

    logger.debug("output: %s", file)
    logger.debug("targets: %s", files)

    if not check_pip():
        install_pip()
    if not check_toml():
        install_toml()

    data = load_toml(file)
    if data is None:
        raise FileNotFoundError(file)

    tomls = [value for file in files if (value := load_toml(file)) is not None]

    if not tomls:
        return

    result = merge_toml(data, *tomls)

    dump_toml(file, result)


if __name__ == "__main__":
    main(*sys.argv[1:])
