#!/bin/bash

while [[ $# -gt 0 ]]; do
  case $1 in
    -m|--mock)
      export FLASK_APP="mock.py"
      shift
      shift
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

# check that .env exists
if [ ! -f ./backend/.env ]; then
  echo "Error: .env file does not exist." >&2
  exit 1
else
  echo ".env file exists"
fi

export PYTHONPATH=$(git rev-parse --show-toplevel)
pushd backend > /dev/null
poetry run flask run --host=0.0.0.0 --port=5001
