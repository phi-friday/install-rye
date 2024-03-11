#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
from os import environ
from pathlib import Path

import merge
from define import call_function_using_sys_argv, ensure_path, set_in_action


def setup_rye_config_use_uv(rye: str, use_uv: str) -> str:
    command = f"{rye} config --set-bool behavior.use-uv={use_uv}"
    subprocess.run(shlex.split(command), check=True)  # noqa: S603

    command = f"{rye} config --get behavior.use-uv"
    process = subprocess.run(
        shlex.split(command),  # noqa: S603
        check=True,
        text=True,
        capture_output=True,
    )

    return process.stdout.strip()


def get_real_rye_config_path(rye: str) -> Path:
    path = ensure_path(rye)
    path = path.resolve()

    return path.parent.with_name("config.toml")


def get_rye_config_path(rye: str) -> Path:
    command = f"{rye} config --show-path"
    process = subprocess.run(
        shlex.split(command),  # noqa: S603
        check=True,
        text=True,
        capture_output=True,
    )
    path = process.stdout.strip()
    path = ensure_path(path)
    return path.resolve()


def setup_python_version(rye: str, python_version: str) -> str:
    command = f"{rye} pin cpython@{python_version}"
    subprocess.run(shlex.split(command), check=True)  # noqa: S603

    python_version_path = Path(".python-version").resolve()
    with python_version_path.open("r") as file:
        text = file.read()
    return text.strip()


def merge_config(rye: str) -> Path:
    default_rye_path = Path(environ["HOME"]).resolve() / ".rye"
    default_rye_path.mkdir(exist_ok=True)
    default_config = default_rye_path / "config.toml"

    config = get_rye_config_path(rye)
    real_config = get_real_rye_config_path(rye)
    merge.main(default_config, real_config, config)

    if default_rye_path == real_config:
        return real_config

    real_config.parent.mkdir(parents=True, exist_ok=True)
    real_config.unlink(missing_ok=True)

    with default_config.open("rb") as default_file:
        config_bytes = default_file.read()

    with real_config.open("wb+") as file:
        file.write(config_bytes)

    return real_config


def get_rye_version(rye: str) -> str:
    command = f"{rye} --version"
    process = subprocess.run(
        shlex.split(command),  # noqa: S603
        check=True,
        text=True,
        capture_output=True,
    )
    output = process.stdout.strip()
    return output.splitlines()[0].split()[1]


def main(rye: str, python_version: str, use_uv: str) -> None:
    use_uv = setup_rye_config_use_uv(rye, use_uv)
    real_config = merge_config(rye)
    rye_home = real_config.parent.as_posix()
    python_version = setup_python_version(rye, python_version)
    rye_version = get_rye_version(rye)

    set_in_action("rye-version", rye_version, "output")
    set_in_action("rye-home", rye_home, "output")
    set_in_action("python-version", python_version, "output")
    set_in_action("use-uv", use_uv, "output")


if __name__ == "__main__":
    call_function_using_sys_argv(main)
