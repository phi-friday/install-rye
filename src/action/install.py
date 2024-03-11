#!/usr/bin/env python3
from __future__ import annotations

import os
import shlex
import subprocess
from http import HTTPStatus
from http.client import HTTPException
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from urllib.request import Request, urlopen

from define import (
    RYE_SCRIPT_URL,
    add_path_in_action,
    call_function_using_sys_argv,
    ensure_path,
    logger,
    set_in_action,
)

if TYPE_CHECKING:
    from http.client import HTTPResponse

__all__ = []


def download_rye_install_script(path: str | Path) -> None:
    path = ensure_path(path)

    response: HTTPResponse
    request = Request(  # noqa: S310
        RYE_SCRIPT_URL,
        headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        },
    )
    with urlopen(request, timeout=5) as response:  # noqa: S310
        if response.status != HTTPStatus.OK:
            raise HTTPException(response.status)
        body = response.read()

    with path.open("wb+") as file:
        file.write(body)


def install_rye(path: str | Path, rye_version: str, rye_home: str | Path) -> None:
    path = ensure_path(path)
    path = path.resolve()

    rye_home = ensure_path(rye_home)
    rye_home = rye_home.resolve()

    path_as_string = path.as_posix()
    rye_home_as_string = rye_home.as_posix()

    envs = {
        "RYE_VERSION": rye_version,
        "RYE_HOME": rye_home_as_string,
        "RYE_INSTALL_OPTION": "--yes",
        "RUST_BACKTRACE": os.getenv("IS_DEBUG", "0"),
    }

    command = f"bash {path_as_string}"
    try:
        process = subprocess.run(
            shlex.split(command),  # noqa: S603
            check=True,
            capture_output=True,
            env=envs,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stdout)
        logger.error(exc.stderr)
        raise

    logger.info(process.stdout)
    stderr = process.stderr.strip()
    if stderr:
        logger.error(stderr)


def main(rye_version: str, rye_home: str | Path) -> None:
    rye_home = ensure_path(rye_home)
    rye_home = rye_home.resolve()

    with TemporaryDirectory(prefix="install_rye_") as temp_dir:
        temp_dir_path = Path(temp_dir)
        rye_script_path = temp_dir_path / "rye.sh"

        download_rye_install_script(rye_script_path)
        install_rye(rye_script_path, rye_version, rye_home)

    shims = rye_home / "shims"
    shims_as_string = shims.as_posix()

    add_path_in_action(shims)
    set_in_action("rye-shims", shims_as_string, "output")


if __name__ == "__main__":
    call_function_using_sys_argv(main)
