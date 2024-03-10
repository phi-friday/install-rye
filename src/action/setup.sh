#!/usr/bin/env bash

# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
MERGE_SCRIPT=${SCRIPTPATH}/merge.py

rye config --set-bool behavior.use-uv=$INPUT_USE_UV
rye pin cpython@$INPUT_PYTHON_VERSION

INSTALLED_RYE_VERSION=$(rye --version | awk '{print $2}' | head -n 1)
INSTALLED_RYE_HOME=$(dirname $(dirname $(which rye)))
PINNED_PYTHON_VERSION=$(cat .python-version)
USE_UV=$(rye config --get behavior.use-uv)
echo "rye-version=${INSTALLED_RYE_VERSION}"    >> $GITHUB_OUTPUT
echo "rye-home=${INSTALLED_RYE_HOME}"          >> $GITHUB_OUTPUT
echo "python-version=${PINNED_PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}"                        >> $GITHUB_OUTPUT

python3 $MERGE_SCRIPT $(rye config --show-path) $HOME/.rye/config.toml