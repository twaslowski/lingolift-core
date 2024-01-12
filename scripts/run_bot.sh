#!/bin/bash

# check that .env exists
if [ ! -f ./telegram_client/.env ]; then
  echo "Error: .env file does not exist." >&2
  exit 1
else
  echo ".env file exists"
fi

# get current directory path
export PYTHONPATH=$(git rev-parse --show-toplevel)
pushd telegram_client > /dev/null
poetry run python app.py
popd
