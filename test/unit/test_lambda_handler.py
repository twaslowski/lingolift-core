import json

from iso639 import LanguageNotFoundError
from shared.exception import ApplicationException, LanguageNotIdentifiedException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

from lingolift.lambda_handlers import (
    literal_translation_handler,
    response_suggestion_handler,
    translation_handler,
)


def test_translation_handler_happy_path(translation_generator):
    event = {"body": json.dumps({"sentence": "test"})}
    response = translation_handler(event, None)
    assert response.get("statusCode") == 200
    t = Translation(**json.loads(response.get("body")))
    assert t.translation == "test"
    assert t.language_name == "test"
    assert t.language_code == "test"


def test_translation_handler_unhappy_path(mocker):
    mocker.patch(
        "lingolift.lambda_functions_generative.generate_translation",
        side_effect=LanguageNotFoundError,
    )

    event = {"body": json.dumps({"sentence": "test"})}
    response = translation_handler(event, None)
    assert response.get("statusCode") == 400
    e = ApplicationException(**json.loads(response.get("body")))
    assert e.error_message == LanguageNotIdentifiedException().error_message


def test_literal_translation_handler_happy_path(mocker):
    mocker.patch(
        "lingolift.lambda_functions_generative.generate_literal_translation",
        return_value=[LiteralTranslation(word="test", translation="test")],
    )
    event = {"body": json.dumps({"sentence": "test"})}
    response = literal_translation_handler(event, None)
    assert response.get("statusCode") == 200
    translations = [LiteralTranslation(**t) for t in json.loads(response.get("body"))]
    assert len(translations) == 1
    assert translations[0].word == "test"
    assert translations[0].translation == "test"


def test_response_suggestions_happy_path(mocker):
    mocker.patch(
        "lingolift.lambda_functions_generative.generate_response_suggestions",
        return_value=[ResponseSuggestion(suggestion="test", translation="test")],
    )
    event = {"body": json.dumps({"sentence": "test"})}
    response = response_suggestion_handler(event, None)
    assert response.get("statusCode") == 200
    suggestions = [ResponseSuggestion(**t) for t in json.loads(response.get("body"))]
    assert len(suggestions) == 1
    assert suggestions[0].suggestion == "test"
    assert suggestions[0].translation == "test"
