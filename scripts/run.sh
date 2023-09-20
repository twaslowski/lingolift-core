if [[ -d venv ]]; then
  echo "virtual environment exists"
else
  python3 -m venv venv
fi

echo "activating virtual environment"
source venv/bin/activate

echo "installing dependencies"
pip install -r requirements.txt

# check that .env exists
if [ ! -f .env ]; then
  echo "Error: .env file does not exist." >&2
  exit 1
else
  echo ".env file exists"
fi

# get current directory path
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
export PYTHONPATH=$PYTHONPATH:$ROOT_DIR

if [[ -n $MOCK ]]; then
  python src/mock.py
else
  python src/main.py
fi
echo $! > .pid