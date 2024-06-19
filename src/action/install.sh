#!/usr/bin/env bash

curl -sSf https://rye.astral.sh/get | bash
echo "${RYE_HOME}/shims" >> $GITHUB_PATH