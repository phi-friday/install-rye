#!/usr/bin/env bash

RYE_VERSION=$(   [    "$INPUT_RYE_VERSION" = "default" ] && echo "latest" || echo "$INPUT_RYE_VERSION")
RYE_HOME=$(      [       "$INPUT_RYE_HOME" = "default" ] && echo       "" || echo "$INPUT_RYE_HOME")
PYTHON_VERSION=$([ "$INPUT_PYTHON_VERSION" = "default" ] && echo   "3.12" || echo "$INPUT_PYTHON_VERSION")
USE_UV=$(        [         "$INPUT_USE_UV" = "default" ] && echo   "true" || echo "$INPUT_USE_UV")

RYE_HOME=$([ -z "$RYE_HOME" ] && echo "$HOME/.rye" || echo "$RYE_HOME")

echo "   rye version: $RYE_VERSION"
echo "      rye home: $RYE_HOME"
echo "python version: $PYTHON_VERSION"
echo "        use uv: $USE_UV"

echo "rye-version=${RYE_VERSION}" >> $GITHUB_OUTPUT
echo "rye-home=${RYE_HOME}" >> $GITHUB_OUTPUT
echo "python-version=${PYTHON_VERSION}" >> $GITHUB_OUTPUT
echo "use-uv=${USE_UV}" >> $GITHUB_OUTPUT