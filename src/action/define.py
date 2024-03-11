from __future__ import annotations

import inspect
import logging
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Callable, Literal  # noqa: UP035

__all__ = [
    "DEFAULT_RYE_VERSION",
    "DEFAULT_RYE_HOME",
    "DEFAULT_PYTHON_VERSION",
    "DEFAULT_USE_UV",
    "DEFAULT_VALUES",
    "RYE_SCRIPT_URL",
    "logger",
    "if_default_set_value",
    "check_variable",
    "ensure_path",
    "set_in_action",
    "set_multiline_in_action",
    "add_path_in_action",
    "call_function_using_sys_argv",
    "inspect_function_variables",
]

_GITHUB_OUTPUT = Path(os.environ["GITHUB_OUTPUT"])
_GITHUB_PATH = Path(os.environ["GITHUB_PATH"])
_GITHUB_ENV = Path(os.environ["GITHUB_ENV"])
_GITHUB_OUTPUTS = Literal["output", "env"]
_GITHUB_OUTPUTS_MAPPING: dict[_GITHUB_OUTPUTS, Path] = {
    "output": _GITHUB_OUTPUT,
    "env": _GITHUB_ENV,
}

DEFAULT_RYE_VERSION = "latest"
DEFAULT_RYE_HOME = ""
DEFAULT_PYTHON_VERSION = "3.12"
DEFAULT_USE_UV = "true"
DEFAULT_VALUES: dict[str, str] = {
    "rye_version": DEFAULT_RYE_VERSION,
    "rye_home": DEFAULT_RYE_HOME,
    "python_version": DEFAULT_PYTHON_VERSION,
    "use_uv": DEFAULT_USE_UV,
}

RYE_SCRIPT_URL = "https://rye-up.com/get"


def get_logger() -> logging.Logger:
    logger = logging.getLogger("install-rye.merge")
    if logger.hasHandlers():
        return logger

    logger.addHandler(logging.StreamHandler(sys.stdout))

    if os.getenv("IS_DEBUG", "0") == "1":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger


def if_default_set_value(
    value: str, if_true: str, if_false: str, default: str = "default"
) -> str:
    return if_true if value == default else if_false


def check_variable(name: str, left: str, right: str) -> None:
    if left == right:
        return

    logger.error("invalid %s: %s != %s", name, left, right)
    sys.exit(1)


def ensure_path(path: str | Path) -> Path:
    if isinstance(path, str):
        return Path(path)
    return path


def set_in_action(name: str, value: str, where: _GITHUB_OUTPUTS) -> None:
    # https://github.com/orgs/community/discussions/28146#discussioncomment-5638023
    path = _GITHUB_OUTPUTS_MAPPING[where]
    logger.debug("set in %s :: name: %s, value: %s", name, value, where)
    with path.open("a") as fh:
        print(f"{name}={value}", file=fh)


def set_multiline_in_action(name: str, value: str, where: _GITHUB_OUTPUTS) -> None:
    # https://github.com/orgs/community/discussions/28146#discussioncomment-5638023
    path = _GITHUB_OUTPUTS_MAPPING[where]
    logger.debug("set in %s :: name: %s, value: %s", name, value, where)
    with path.open("a") as fh:
        delimiter = uuid.uuid1()
        print(f"{name}<<{delimiter}", file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)


def add_path_in_action(path: str | Path) -> None:
    path = ensure_path(path)
    path = path.resolve()
    path_as_string = path.as_posix()

    logger.info("add path: %s", path)
    with _GITHUB_PATH.open("a") as fh:
        print(path_as_string, file=fh)


def inspect_param_length(func: Callable[..., Any]) -> int:
    signature = inspect.signature(func)
    return len(signature.parameters)


def call_function_using_sys_argv(func: Callable[..., Any]) -> None:
    size = inspect_param_length(func)
    return func(*sys.argv[1 : 1 + size])


def inspect_function_variables() -> dict[str, Any]:
    frame = inspect.currentframe()
    assert frame is not None  # noqa: S101
    frame = frame.f_back
    assert frame is not None  # noqa: S101
    arg_info = inspect.getargvalues(frame)
    return {x: arg_info.locals[x] for x in arg_info.args}


logger = get_logger()
