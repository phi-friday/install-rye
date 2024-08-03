#!/usr/bin/env bash

rye pin cpython@$INPUT_PYTHON_VERSION
rye fetch

INSTALLED_RYE_HOME=$(dirname $(dirname $(which rye)))
INSTALLED_RYE_VERSION=$(rye --version | awk '{print $2}' | head -n 1)
PINNED_PYTHON_VERSION=$(cat .python-version)
echo "rye-version=${INSTALLED_RYE_VERSION}"    >> $GITHUB_OUTPUT
echo "rye-home=${INSTALLED_RYE_HOME}"          >> $GITHUB_OUTPUT
echo "python-version=${PINNED_PYTHON_VERSION}" >> $GITHUB_OUTPUT