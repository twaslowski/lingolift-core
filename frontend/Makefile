.PHONY: test run lint shared

test:
	@poetry run pytest

run:
	@poetry run streamlit run GrammrBot.py local

lint:
	@poetry run mypy .

shared:
	@poetry remove shared && poetry add ../shared/

fmt:
	@pre-commit run black --all-files
	@pre-commit run end-of-file-fixer --all-files
