#!/usr/bin/env python3
import inspect
from os import environ

from define import (
    DEFAULT_PYTHON_VERSION,
    DEFAULT_RYE_HOME,
    DEFAULT_RYE_VERSION,
    DEFAULT_USE_UV,
    call_function_using_sys_argv,
    if_default_set_value,
    set_in_action,
)


def main(rye_version: str, rye_home: str, python_version: str, use_uv: str) -> None:
    signature = inspect.signature(main)
    params: dict[str, str] = dict(
        signature.bind(rye_version, rye_home, python_version, use_uv).arguments
    )

    home = environ["HOME"]

    for (key, value), (default) in zip(
        tuple(params.items()),
        (DEFAULT_RYE_VERSION, DEFAULT_RYE_HOME, DEFAULT_PYTHON_VERSION, DEFAULT_USE_UV),
    ):
        params[key] = if_default_set_value(value, default, value)

    params["rye_home"] = if_default_set_value(
        params["rye_home"].strip(), f"{home}/.rye", params["rye_home"], ""
    )

    for key, value in params.items():
        output_key = key.replace("_", "-")
        set_in_action(output_key, value, "output")


if __name__ == "__main__":
    call_function_using_sys_argv(main)
