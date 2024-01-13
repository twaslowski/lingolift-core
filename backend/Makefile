phony: test export_pythonpath

run: export_pythonpath
	@poetry run flask run app.py --host=0.0.0.0 --port=5001

mock: export_pythonpath
	@poetry run flask run mock.py --host=0.0.0.0 --port=5001

test: export_pythonpath
	@pytest

export_pythonpath:
	# required for shared/ right now, this is a terrible hack though
	@export PYTHONPATH=./

check_dotenv:
	# todo
	@[ ! -f ./backend/.env ]