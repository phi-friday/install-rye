#!/usr/bin/env python3
from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import toml  # pyright: ignore[reportMissingModuleSource]

logger = logging.getLogger("install-rye.merge")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)


def load_toml(path: str | Path) -> dict[str, Any] | None:
    """toml to dict or null"""

    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()

    if not path.exists():
        logger.info("there is no file: %s", path)
        return None

    with path.open("r") as file:
        result = toml.load(file)

    logger.info("path: %s, data: %s", path, result)
    return result


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

    if isinstance(path, str):
        path = Path(path)
    path = path.resolve()

    with path.open("w+") as file:
        toml.dump(data, file)


def main(file: str | Path, *files: str | Path) -> None:  # noqa: D103
    logger.info("output: %s", file)
    logger.info("targets: %s", files)

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
