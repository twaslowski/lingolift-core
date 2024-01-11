#!/bin/bash

if [[ -d telegram_client/venv ]]; then
  echo "virtual environment exists"
else
  python3 -m venv telegram_client/venv
fi

echo "activating virtual environment"
source telegram_client/venv/bin/activate

echo "installing dependencies"
pip install -r telegram_client/requirements.txt

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
