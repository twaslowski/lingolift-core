# Webserver docker image to emulate the API Gateway endpoints for the frontend
FROM weastur/poetry:1.8.3-python-3.12-slim

WORKDIR /app

# On macOS, AirPlay Receiver runs on 5000 by default, which interferes with Flask
# This breaks convention, but may be more convenient for macOS developers
EXPOSE 5001

# Environment variables
ENV OPENAI_API_KEY="sk-replace-me"
ENV PYTHONPATH=/app
ENV FLASK_APP=lingolift/webserver.py

# And corresponding spacy model id, e.g. "en_core_web_sm"
ARG SPACY_MODEL
ENV SPACY_MODEL=${SPACY_MODEL}

# Verify that neither values are empty
RUN test -n "${SPACY_MODEL}"

# Copy source files
COPY pyproject.toml poetry.lock ./
COPY lingolift ./lingolift

RUN poetry install --no-root --without dev
RUN poetry run spacy download ${SPACY_MODEL}

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5001"]
