#!/usr/bin/env python3
import inspect
from os import environ

from define import (
    DEFAULT_VALUES,
    call_function_using_sys_argv,
    if_default_set_value,
    inspect_function_variables,
    logger,
    set_in_action,
)


def main(
    rye_version: str, rye_home: str, python_version: str, use_uv: str
) -> dict[str, str]:
    signature = inspect.signature(main)
    args = inspect_function_variables()
    params: dict[str, str] = dict(signature.bind(**args).arguments)

    home = environ["HOME"]

    for key, value in tuple(params.items()):
        default = DEFAULT_VALUES[key]
        params[key] = if_default_set_value(value, default, value)

    params["rye_home"] = if_default_set_value(
        params["rye_home"].strip(), f"{home}/.rye", params["rye_home"], ""
    )

    for key, value in params.items():
        logger.info("%s: %s", key.replace("_", " "), value)
        output_key = key.replace("_", "-")
        set_in_action(output_key, value, "output")

    return params


if __name__ == "__main__":
    call_function_using_sys_argv(main)
