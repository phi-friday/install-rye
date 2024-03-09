#!/usr/bin/env bash
# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DEFINE_SCRIPT=${SCRIPTPATH}/prepare.sh

source $DEFINE_SCRIPT

RYE_VERSION=$(    set_default $INPUT_RYE_VERSION    $DEFAULT_RYE_VERSION    )
RYE_HOME=$(       set_default $INPUT_RYE_HOME       $DEFAULT_RYE_HOME       )
PYTHON_VERSION=$( set_default $INPUT_PYTHON_VERSION $DEFAULT_PYTHON_VERSION )
USE_UV=$(         set_default $INPUT_USE_UV         $DEFAULT_USE_UV         )

RYE_HOME=$([ -z "$RYE_HOME" ] && echo "$HOME/.rye" || echo "$RYE_HOME")

echo "   rye version: $RYE_VERSION"
echo "      rye home: $RYE_HOME"
echo "python version: $PYTHON_VERSION"
echo "        use uv: $USE_UV"

echo "rye-version=${RYE_VERSION}" >> $GITHUB_OUTPUT
echo "rye-home=${RYE_HOME}" >> $GITHUB_OUTPUT
echo "python-version=${PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}" >> $GITHUB_OUTPUT