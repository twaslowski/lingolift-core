from unittest import TestCase

from shared.model.error import LingoliftError
from shared.model.literal_translation import LiteralTranslation
from shared.model.syntactical_analysis import SyntacticalAnalysis

from app import app


class TestApp(TestCase):

    def test_literal_translation_returns_error_if_too_many_unique_words(self):
        client = app.test_client()
        response = client.post("http://localhost:5001/literal-translation", json={
            "sentence": "this sentence is too long because it contains too many unique words a b c d e f"})
        self.assertEqual(response.status_code, 400)
        print(response.json)
        # implicitely checks that the response is a LingoliftError; no assertion because
        LingoliftError(**response.json)

    def test_literal_translation_happy_path(self):
        client = app.test_client()
        response = client.post("http://localhost:5001/literal-translation", json={
            "sentence": "test sentence"})
        self.assertEqual(response.status_code, 200)
        for r in response.json:
            LiteralTranslation(**r)

    def test_syntactical_analysis(self):
        client = app.test_client()
        response = client.post("http://localhost:5001/syntactical-analysis", json={
            "sentence": "test sentence",
            "language": "russian"})
        self.assertEqual(response.status_code, 200)
        for a in response.json:
            SyntacticalAnalysis(**a)

    def test_syntactical_analysis_error(self):
        client = app.test_client()
        response = client.post("http://localhost:5001/syntactical-analysis", json={
            "sentence": "test sentence",
            "language": "non-existent-language"})
        self.assertEqual(response.status_code, 400)
        LingoliftError(**response.json)
