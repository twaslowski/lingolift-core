phony: test export_pythonpath

test: export_pythonpath
	@poetry run python -m unittest

run: export_pythonpath
	@poetry run streamlit run app.py

export_pythonpath:
	@export PYTHONPATH=$(git rev-parse --show-toplevel)
