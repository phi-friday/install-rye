#!/usr/bin/env bash

# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DEFINE_SCRIPT=${SCRIPTPATH}/define.sh
PREPARE_SCRIPT=${SCRIPTPATH}/prepare.sh

source $DEFINE_SCRIPT

echo "input:"
echo "   rye version: ${INPUT_RYE_VERSION}"
echo "      rye home: ${INPUT_RYE_HOME}"
echo "python version: ${INPUT_PYTHON_VERSION}"

INPUT_RYE_VERSION=$(    set_default $INPUT_RYE_VERSION    $REAL_RYE_VERSION    )
INPUT_RYE_HOME=$(       set_default $INPUT_RYE_HOME       $REAL_RYE_HOME       )
INPUT_PYTHON_VERSION=$( set_default $INPUT_PYTHON_VERSION $REAL_PYTHON_VERSION )

echo "expected:"
source $PREPARE_SCRIPT

echo "real:"
echo "   rye version: ${REAL_RYE_VERSION}"
echo "      rye home: ${REAL_RYE_HOME}"
echo "python version: ${REAL_PYTHON_VERSION}"

check_variable "rye version"    $RYE_VERSION    $REAL_RYE_VERSION
check_variable "rye home"       $RYE_HOME       $REAL_RYE_HOME
check_variable "python version" $PYTHON_VERSION $REAL_PYTHON_VERSION