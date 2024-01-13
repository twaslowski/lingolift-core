from unittest import TestCase

import pytest
import requests

from backend.app import app
from shared.model.error import LingoliftError


class TestApp(TestCase):

    @pytest.fixture()
    def client(self):
        return app.test_client()

    def test_literal_translation_returns_error_if_too_many_unique_words(self):
        client = app.test_client()
        response = client.post("http://localhost:5001/literal-translation", json={
            "sentence": "this sentence is too long because it contains too many unique words a b c d e f"})
        self.assertEqual(response.status_code, 400)
        print(response.json)
        # implicitely checks that the response is a LingoliftError; no assertion because
        LingoliftError(**response.json)
