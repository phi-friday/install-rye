#!/usr/bin/env bash

curl -sSf https://rye-up.com/get | bash
echo "${RYE_HOME}/shims" >> $GITHUB_PATH