import json

from test.integration.conftest import set_llm_response

from shared.exception import ApplicationException, LanguageNotIdentifiedException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

from lingolift.core_lambda_handlers import (
    literal_translation_handler,
    response_suggestion_handler,
    translation_handler,
)
from lingolift.nlp_lambda_handlers import (
    syntactical_analysis_handler,
)


def test_translation_handler_happy_path(core_context_container):
    # Given the LLM Adapter returns a translation
    set_llm_response(
        core_context_container,
        json.dumps({"translation": "Where is the Library?", "language_code": "ES"}),
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


def test_translation_handler_language_not_identified(core_context_container):
    # Given the LLM Adapter returns a language not identified exception
    set_llm_response(
        core_context_container,
        json.dumps(
            {
                "translation": "Where is the Library?",
                "language_code": "XY",
            }
        ),
    )

    event = {"body": json.dumps({"sentence": "test"})}
    response = translation_handler(event, None)
    assert response.get("statusCode") == 400
    e = ApplicationException(**json.loads(response.get("body")))
    assert e.error_message == LanguageNotIdentifiedException().error_message


def test_literal_translation_handler_happy_path(core_context_container):
    # Given the LLM Adapter returns a literal translation
    set_llm_response(
        core_context_container, json.dumps([{"word": "test", "translation": "test"}])
    )

    # When a literal translation request is received
    event = {"body": json.dumps({"sentence": "test"})}
    response = literal_translation_handler(event, None)

    # Then the literal translation is successful
    assert response.get("statusCode") == 200
    translations = [LiteralTranslation(**t) for t in json.loads(response.get("body"))]
    assert len(translations) == 1
    assert translations[0].word == "test"
    assert translations[0].translation == "test"


def test_response_suggestions_happy_path(core_context_container):
    # Given the LLM Adapter returns a response suggestion
    set_llm_response(
        core_context_container,
        json.dumps(
            {
                "response_suggestions": [
                    {"suggestion": "test", "translation": "test"},
                ]
            }
        ),
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


def test_pre_warm_syntactical_analysis(pre_warm_event):
    response = syntactical_analysis_handler(pre_warm_event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"pre-warmed": "true"}


def test_syntactical_analysis_real_event(real_event):
    response = syntactical_analysis_handler(real_event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body) == 4
