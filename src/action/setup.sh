#!/usr/bin/env bash

# https://stackoverflow.com/a/4774063
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
MERGE_SCRIPT=${SCRIPTPATH}/merge.py

echo $INPUT_PYTHON_VERSION >> .python-version
rye config --set-bool behavior.use-uv=$INPUT_USE_UV

INSTALLED_RYE_HOME=$(dirname $(dirname $(which rye)))
RYE_CONFIG_PATH=$(rye config --show-path)
INSTALLED_RYE_CONFIG_PATH=$INSTALLED_RYE_HOME/config.toml
python3 $MERGE_SCRIPT $HOME/.rye/config.toml $RYE_CONFIG_PATH $INSTALLED_RYE_CONFIG_PATH
if [ "$HOME/.rye/config.toml" != "$INSTALLED_RYE_CONFIG_PATH" ]; then
    [ -e $INSTALLED_RYE_CONFIG_PATH ] && rm $INSTALLED_RYE_CONFIG_PATH
    cp $HOME/.rye/config.toml $INSTALLED_RYE_CONFIG_PATH
fi


rye pin cpython@$INPUT_PYTHON_VERSION

INSTALLED_RYE_VERSION=$(rye --version | awk '{print $2}' | head -n 1)
PINNED_PYTHON_VERSION=$(cat .python-version)
USE_UV=$(rye config --get behavior.use-uv)
echo "rye-version=${INSTALLED_RYE_VERSION}"    >> $GITHUB_OUTPUT
echo "rye-home=${INSTALLED_RYE_HOME}"          >> $GITHUB_OUTPUT
echo "python-version=${PINNED_PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}"                        >> $GITHUB_OUTPUT