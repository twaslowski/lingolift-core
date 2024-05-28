import json

import pytest
from shared.exception import LanguageNotAvailableException
from shared.model.inflection import Inflections
from shared.model.syntactical_analysis import PartOfSpeech

from lingolift.lambda_handlers import inflection_handler, syntactical_analysis_handler


@pytest.fixture
def real_event():
    return {
        # one event for both lambdas; additional fields don't cause issues
        "body": json.dumps({"sentence": "This is a test.", "word": "test"})
    }


@pytest.fixture
def pre_warm_event():
    return {"body": json.dumps({"pre_warm": "true"})}


@pytest.fixture
def inflections():
    return Inflections(
        pos=PartOfSpeech(value="VERB", explanation=""), gender=None, inflections=[]
    )


def test_pre_warm_syntactical_analysis(pre_warm_event, mocker):
    mocker.patch("lingolift.lambda_functions_nlp.perform_analysis", return_value=None)
    response = syntactical_analysis_handler(pre_warm_event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"pre-warmed": "true"}

    lambda_functions_nlp.perform_analysis.assert_not_called()


def test_syntactical_analysis_regular_call(real_event, mocker):
    mocker.patch("lingolift.lambda_functions_nlp.perform_analysis", return_value=[])
    response = syntactical_analysis_handler(real_event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == []

    lambda_functions_nlp.perform_analysis.assert_called_once()


def test_syntactical_analysis_regular_call_with_exception(real_event, mocker):
    mocker.patch(
        "lambda_functions_nlp.perform_analysis",
        side_effect=LanguageNotAvailableException(),
    )
    response = syntactical_analysis_handler(real_event, None)

    assert response["statusCode"] == 400
    assert "error_message" in json.loads(response["body"])

    lambda_functions_nlp.perform_analysis.assert_called_once()


def test_pre_warm_inflection(pre_warm_event, mocker):
    response = inflection_handler(pre_warm_event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"pre-warmed": "true"}


def test_inflection_regular_call(real_event, mocker, inflections):
    mocker.patch(
        "lambda_functions_nlp.retrieve_all_inflections",
        return_value=inflections,
    )
    response = inflection_handler(real_event, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == inflections.model_dump()

    lambda_handler.retrieve_all_inflections.assert_called_once()
