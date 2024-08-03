#!/usr/bin/env bash

DEFAULT_RYE_VERSION="latest"
DEFAULT_RYE_HOME=""
DEFAULT_PYTHON_VERSION="3.12"

function set_default {
    [ "$1" = "default" ] && echo "$2" || echo "$1"
}

function check_variable {
    if [[ "$2" != "$3"    ]]; then 
        echo "invalid $1: $2 != $3"
        exit 1;
    fi
}