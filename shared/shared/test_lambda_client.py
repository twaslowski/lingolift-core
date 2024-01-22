import json
from unittest.mock import Mock

import pytest

from shared.exception import ApplicationException
from shared.lambda_client import LambdaClient

"""
Tests the shared client methods that are used by both the frontend and the telegram bot.
This only tests for happy paths (200 status codes),
expected errors (400 status codes with the backend error object),
and unexpected errors (500 status codes). There is no need to test for JSON structure as the backend only
sends responses that adhere to the shared pydantic models defined in the `shared.model` package.
"""


def test_translation_happy_path(mocker):
    # Set up mocks
    mock_payload = Mock()
    mock_payload.read.return_value = ('{"status_code": 200, "body": '
                                      '{"translation": "some translation", '
                                      '"language_name": "test", '
                                      '"language_code": "test"}}')

    # Set up client
    client = LambdaClient("some", "credentials", "here")
    # Patch the lambda_client's invoke method
    mocker.patch.object(client.lambda_client, 'invoke', return_value={"Payload": mock_payload})

    # when
    translation = client.fetch_translation("some sentence")

    # then
    assert translation.translation == "some translation"
    assert translation.language_name == "test"
    assert translation.language_code == "test"


def test_translation_expected_error(mocker):
    # Set up mocks
    mock_payload = Mock()
    mock_payload.read.return_value = (json.dumps({
        "status_code": 400,
        "body": ApplicationException("some error").dict()
    }))

    # Set up client
    client = LambdaClient("some", "credentials", "here")
    # Patch the lambda_client's invoke method
    mocker.patch.object(client.lambda_client, 'invoke', return_value={"Payload": mock_payload})

    with pytest.raises(ApplicationException) as e:
        client.fetch_translation("some sentence")
        captured_error = ApplicationException(**e.value)
        assert captured_error.error_message == "some error"


def test_translation_unexpected_error(mocker):
    mock_payload = Mock()
    mock_payload.read.return_value = (json.dumps({
        "status_code": 500,
        "body": ApplicationException("some error").dict()
    }))

    client = LambdaClient("some", "credentials", "here")
    mocker.patch.object(client.lambda_client, 'invoke', return_value={"Payload": mock_payload})

    with pytest.raises(ApplicationException) as e:
        client.fetch_translation("some sentence")
        captured_error = ApplicationException(**e.value)
        assert captured_error.error_message == "Unknown error occurred."
