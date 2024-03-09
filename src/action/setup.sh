#!/usr/bin/env bash

rye config --set-bool behavior.use-uv=$INPUT_USE_UV
rye pin cpython@$INPUT_PYTHON_VERSION

INSTALLED_RYE_VERSION=$(rye --version | awk '{print $2}' | head -n 1)
PINNED_PYTHON_VERSION=$(cat .python-version)
USE_UV=$(rye config --get behavior.use-uv)
echo "rye-version=${INSTALLED_RYE_VERSION}"    >> $GITHUB_OUTPUT
echo "python-version=${PINNED_PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}"                        >> $GITHUB_OUTPUT