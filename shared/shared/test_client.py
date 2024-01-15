from unittest import TestCase
from unittest.mock import Mock
import pytest

import requests

from shared.client import Client, TRANSLATIONS_UNEXPECTED_ERROR


class TestClient(TestCase):
    """
    Tests the shared client methods that are used by both the frontend and the telegram bot.
    This only tests for happy paths (200 status codes),
    expected errors (400 status codes with the Lingolift error object),
    and unexpected errors (500 status codes). There is no need to test for JSON structure as the backend only
    sends responses that adhere to the shared pydantic models defined in the `shared.model` package.
    """

    def setUp(self) -> None:
        requests.post = Mock()
        self.client = Client()

    def test_translation_happy_path(self):
        # when posting to /translation, we receive a well-formed translation json with a 200 OK status code
        requests.post = Mock()
        requests.post.return_value.status_code = 200
        requests.post.return_value.json.return_value = {
            "translation": "translation",
            "language": "language"
        }
        translation = self.client.fetch_translation("some sentence")
        self.assertEqual(translation.translation, "translation")
        self.assertEqual(translation.language, "language")

    def test_translation_unexpected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 500
        requests.post.return_value.json.return_value = None
        error = self.client.fetch_translation("some sentence")
        self.assertEqual(error.error_message, TRANSLATIONS_UNEXPECTED_ERROR)

    def test_literal_translation_happy_path(self):
        pass

    def test_literal_translation_expected_error(self):
        pass

    def test_literal_translation_unexpected_error(self):
        pass

    def test_syntactical_analysis_happy_path(self):
        # test 200
        pass

    def test_syntactical_analysis_expected_error(self):
        # test expected 400
        pass

    def test_syntactical_analysis_unexpected_error(self):
        # test unexpected status codes
        pass
