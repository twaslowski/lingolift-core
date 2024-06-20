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

# Define source language
ARG SOURCE_LANG
ENV SOURCE_LANG=${SOURCE_LANG}

# Copy files
COPY pyproject.toml poetry.lock ./
COPY lingolift ./lingolift

RUN poetry install --no-root --with webserver --with nlp

ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5001"]
