# lingolift-backend

This codebase serves the lingolift HTTP backend on which several types of clients can be run.
It accepts requests on several endpoints to perform different functionalities related to translating
and analysing sentences from arbitrary languages.

## Running

### Quick Start

To initially set up the project, do the following:

`git clone git@github.com:TobiasWaslowski/lingolift.git && cd lingolift/backend`

You should have an OpenAI API key for this. If you want to, you can modify `gpt_adapter.py` to use a local model
for inference or alternative services like Mistral, Cohere or others.

`echo "OPENAI_API_KEY=sk-your-openai-api-key > .env`

`poetry install`

`make run`

This will launch a Flask server against which you can perform requests.

### Docker

You can dockerize the application, which is highly recommended for deploying to different systems.
To achieve this, simply run `docker build .`

todo: the Dockerfile has not been migrated to Poetry yet.
todo: currently, the .env file is being copied into the image. Pass it as an environment variable instead.

## Testing

Although test coverage is lacking in parts of the codebase, there are several unit and integration tests available.
The applications endpoints are tested (`test_app.py`) and benchmarks for LLMs exist (`test_benchmark.py`).
This allows for verifying the structural integrity and quality of LLM responses and will safely allow anyone
to migrate to different inference engines if required.

You can run unit tests with `make test`, and more complex integration tests with `make integration-test`.

## Endpoint Documentation

There are four endpoints available as of now:

### Translation

This endpoint provides translations of arbitrary sentences alongside language classification.
Language classification enables syntactical analysis of sentences using spaCy further down the line.

**Request**

    POST /translation -d {
        "sentence": "¿Donde esta la biblioteca?"
    }

**Response**

    200 OK, {
        "translation": "Where is the library",
        "language": "spanish"
    }

### Literal Translations

This endpoint provides literal translations for every unique word in a sentence. It guarantees that all words are
translated unambiguously.

**Request**

    POST /translation -d {
        "sentence": "¿Donde esta la biblioteca?"
    }

**Response**

    200 OK, [
        {
            "word": "donde",
            "translation": "where"
        },
        {
        "word": "esta",
        "translation": "is"
        },
        ...
    ]

### Syntactical analysis

This endpoint provides what is essential part-of-speech tagging using the spaCy NLP library.
It is important to provide the language, because spaCy uses different models for each language, which have to be loaded.

If no model is found to perform the syntactical analysis with, a response with a `400` status code and an error message
will be returned.

**Request**

    POST /syntactical-analysis -d {
        "sentence": "¿Donde esta la biblioteca?",
        "language": "Spanish"
    }

**Response**

    200 0K, [
        {
            "dependencies": "biblioteca",
            "lemma": "donde",
            "morphology": "PronType=Ind",
            "word": "donde"
            },
            {
            "dependencies": "biblioteca",
            "lemma": "este",
            "morphology": "Gender=Fem|Number=Sing|PronType=Dem",
            "word": "esta"
            },
        ...
    ]

