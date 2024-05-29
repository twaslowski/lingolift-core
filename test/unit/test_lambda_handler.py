import json
from test.mock_llm_adapter import MockLLMAdapter
from unittest.mock import patch

import pytest
from iso639 import LanguageNotFoundError
from shared.exception import ApplicationException, LanguageNotIdentifiedException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

import lingolift.lambda_handlers
from lingolift.lambda_context_container import ContextContainer
from lingolift.lambda_handlers import (
    literal_translation_handler,
    response_suggestion_handler,
    translation_handler,
)


@pytest.fixture
def mock_llm_adapter():
    return lambda: MockLLMAdapter()


@pytest.fixture
def context_container(mock_llm_adapter):
    context_container = ContextContainer(mock_llm_adapter)
    with patch.object(
        lingolift.lambda_handlers, "context_container", context_container
    ):
        yield context_container


def set_llm_response(context_container: ContextContainer, response: list | dict):
    """
    Set the response for the mocked LLM Adapter.
    :param context_container: context container holding the LLM adapter and wider application context
    :param response: JSON-like object
    :return:
    """
    context_container.llm_adapter.next_response(json.dumps(response))  # noqa


def test_translation_handler_happy_path(context_container):
    # Given the LLM Adapter returns a translation
    set_llm_response(
        context_container,
        {"translation": "Where is the Library?", "language_code": "ES"},
    )

    # When a translation request is received
    event = {"body": json.dumps({"sentence": "test"})}
    response = translation_handler(event, None)

    # Then the translation is sucessful
    assert response.get("statusCode") == 200
    t = Translation(**json.loads(response.get("body")))
    assert t.translation == "Where is the Library?"
    assert t.language_name == "Spanish"
    assert t.language_code == "ES"


@pytest.mark.skip(
    "Dependency inversion for language code operations not implemented yet"
)
def test_translation_handler_unhappy_path(mocker):
    mocker.patch(
        "lingolift.lambda_functions.generate_translation",
        side_effect=LanguageNotFoundError,
    )

    event = {"body": json.dumps({"sentence": "test"})}
    response = translation_handler(event, None)
    assert response.get("statusCode") == 400
    e = ApplicationException(**json.loads(response.get("body")))
    assert e.error_message == LanguageNotIdentifiedException().error_message


def test_literal_translation_handler_happy_path(context_container):
    # Given the LLM Adapter returns a literal translation
    set_llm_response(context_container, [{"word": "test", "translation": "test"}])

    # When a literal translation request is received
    event = {"body": json.dumps({"sentence": "test"})}
    response = literal_translation_handler(event, None)

    # Then the literal translation is successful
    assert response.get("statusCode") == 200
    translations = [LiteralTranslation(**t) for t in json.loads(response.get("body"))]
    assert len(translations) == 1
    assert translations[0].word == "test"
    assert translations[0].translation == "test"


def test_response_suggestions_happy_path(context_container):
    # Given the LLM Adapter returns a response suggestion
    set_llm_response(
        context_container,
        {
            "response_suggestions": [
                {"suggestion": "test", "translation": "test"},
            ]
        },
    )

    # When a response suggestion request is received
    event = {"body": json.dumps({"sentence": "test"})}
    response = response_suggestion_handler(event, None)

    # Then the whole request process is successful
    assert response.get("statusCode") == 200
    suggestions = [ResponseSuggestion(**t) for t in json.loads(response.get("body"))]
    assert len(suggestions) == 1
    assert suggestions[0].suggestion == "test"
    assert suggestions[0].translation == "test"
