phony: test export_pythonpath

run: export_pythonpath
	@poetry run flask run app.py --host=0.0.0.0 --port=5001

mock: export_pythonpath
	@poetry run flask run mock.py --host=0.0.0.0 --port=5001

test: export_pythonpath
	# todo
	@poetry run python -m unittest

export_pythonpath:
	@export PYTHONPATH=$(git rev-parse --show-toplevel)

check_dotenv:
	# todo
	@[ ! -f ./backend/.env ]