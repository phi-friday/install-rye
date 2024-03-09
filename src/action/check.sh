#!/usr/bin/env bash

function check_variable {
    if [[ "$2" != "$3"    ]]; then 
        echo "invalid $1: $2 != $3"
        exit 1;
    fi
}

# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PREPARE_SCRIPT=${SCRIPTPATH}/prepare.sh

echo "expected:"
source $PREPARE_SCRIPT

echo "real:"
echo "   rye version: ${REAL_RYE_VERSION}"
echo "      rye home: ${REAL_RYE_HOME}"
echo "python version: ${REAL_PYTHON_VERSION}"
echo "        use uv: ${REAL_USE_UV}"

check_variable "rye version"    $RYE_VERSION    $REAL_RYE_VERSION
check_variable "rye home"       $RYE_HOME       $REAL_RYE_HOME
check_variable "python version" $PYTHON_VERSION $REAL_PYTHON_VERSION
check_variable "use uv"         $USE_UV         $REAL_USE_UV