#!/usr/bin/env bash

function set_default {
    [ "$1" = "default" ] && echo "$2" || echo "$1"
}

RYE_VERSION=$(    set_default $INPUT_RYE_VERSION    "latest" )
RYE_HOME=$(       set_default $INPUT_RYE_HOME       ""       )
PYTHON_VERSION=$( set_default $INPUT_PYTHON_VERSION "3.12"   )
USE_UV=$(         set_default $INPUT_USE_UV         "true"   )

RYE_HOME=$([ -z "$RYE_HOME" ] && echo "$HOME/.rye" || echo "$RYE_HOME")

echo "   rye version: $RYE_VERSION"
echo "      rye home: $RYE_HOME"
echo "python version: $PYTHON_VERSION"
echo "        use uv: $USE_UV"

echo "rye-version=${RYE_VERSION}" >> $GITHUB_OUTPUT
echo "rye-home=${RYE_HOME}" >> $GITHUB_OUTPUT
echo "python-version=${PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}" >> $GITHUB_OUTPUT