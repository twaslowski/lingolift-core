#!/bin/bash

if [[ -d venv ]]; then
  echo "virtual environment exists"
else
  python3 -m venv venv
fi

echo "activating virtual environment"
source venv/bin/activate

# check that .env exists
if [ ! -f ./telegram_client/.env ]; then
  echo "Error: .env file does not exist." >&2
  exit 1
else
  echo ".env file exists"
fi

# get current directory path
export PYTHONPATH=$(git rev-parse --show-toplevel)
python telegram_client/app.py
