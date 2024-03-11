#!/usr/bin/env python3
import inspect

import prepare
from define import (
    call_function_using_sys_argv,
    check_variable,
    if_default_set_value,
    inspect_function_variables,
    logger,
)

SEPARATOR = ":"


def main(rye_version: str, rye_home: str, python_version: str, use_uv: str) -> None:
    signature = inspect.signature(main)
    args = inspect_function_variables()
    params: dict[str, str] = dict(signature.bind(**args).arguments)

    inputs: dict[str, str] = {}
    prepare_data: dict[str, str] = {}
    result: dict[str, str] = {}

    logger.info("input:")
    for key, value in params.items():
        inputs[key], result[key] = input_value, result_value = value.split(SEPARATOR, 1)
        logger.info("%s: %s", key, input_value)

        prepare_data[key] = if_default_set_value(input_value, input_value, result_value)

    logger.info("\nexpected:")
    prepare_data = prepare.main(**prepare_data)

    logger.info("\nreal:")
    for key, value in tuple(result.items()):
        logger.info("%s: %s", key, value)

    for key in params:
        check_variable(key, prepare_data[key], result[key])


if __name__ == "__main__":
    call_function_using_sys_argv(main)
