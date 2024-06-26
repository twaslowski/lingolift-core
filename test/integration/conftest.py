import json
from test.mock_llm_adapter import MockLLMAdapter
from unittest.mock import patch

import pytest

from lingolift import core_lambda_handlers
from lingolift.abstract_context_container import AbstractLambdaContextContainer
from lingolift.core_lambda_context_container import CoreLambdaContextContainer


def set_llm_response(context_container: AbstractLambdaContextContainer, response: str):
    """
    Set the response for the mocked LLM Adapter.
    :param context_container: context container holding the LLM adapter and wider application context
    :param response: arbitrary string
    :return:
    """
    context_container.llm_adapter.next_response(response)


@pytest.fixture(autouse=True)
def spacy_model_env(monkeypatch):
    monkeypatch.setenv("SPACY_MODEL", "de_core_news_sm")


@pytest.fixture
def mock_llm_adapter():
    return MockLLMAdapter()


@pytest.fixture
def core_context_container(mock_llm_adapter):
    context_container = CoreLambdaContextContainer(mock_llm_adapter)
    with patch.object(core_lambda_handlers, "context_container", context_container):
        yield context_container


@pytest.fixture
def real_event():
    return {
        # one event for both lambdas; additional fields don't cause issues
        "body": json.dumps(
            {"sentence": "Das ist ein Test", "word": "Test", "language_code": "DE"}
        )
    }


@pytest.fixture
def pre_warm_event():
    return {"body": json.dumps({"pre_warm": "true"})}
