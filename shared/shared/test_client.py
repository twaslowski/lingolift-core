from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

import requests  # type: ignore[import-untyped]

from shared.client import Client, TRANSLATIONS_UNEXPECTED_ERROR, LITERAL_TRANSLATIONS_UNEXPECTED_ERROR, \
    SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR, UPOS_EXPLANATIONS_UNEXPECTED_ERROR
from shared.exception import ApplicationException
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation
from shared.model.upos_explanation import UposExplanation


class TestClient(IsolatedAsyncioTestCase):
    """
    Tests the shared client methods that are used by both the frontend and the telegram bot.
    This only tests for happy paths (200 status codes),
    expected errors (400 status codes with the backend error object),
    and unexpected errors (500 status codes). There is no need to test for JSON structure as the backend only
    sends responses that adhere to the shared pydantic models defined in the `shared.model` package.
    """

    def setUp(self) -> None:
        requests.post = Mock()
        self.client = Client()

    async def test_translation_happy_path(self):
        # when posting to /translation, we receive a well-formed translation json with a 200 OK status code
        requests.post = Mock()
        requests.post.return_value.status_code = 200
        requests.post.return_value.json.return_value = {
            "translation": "translation",
            "language_name": "german",
            "language_code": "de"
        }
        translation = await self.client.fetch_translation("some sentence")
        self.assertIsInstance(translation, Translation)
        self.assertEqual(translation.translation, "translation")
        self.assertEqual(translation.language_name, "german")
        self.assertEqual(translation.language_code, "de")

    async def test_translation_unexpected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 500
        requests.post.return_value.json.return_value = None
        error = await self.client.fetch_translation("some sentence")
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, TRANSLATIONS_UNEXPECTED_ERROR)

    async def test_literal_translation_happy_path(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 200
        requests.post.return_value.json.return_value = [
            {
                "word": "some",
                "translation": "ein"
            },
            {
                "word": "sentence",
                "translation": "satz"
            }
        ]
        literal_translations = await self.client.fetch_literal_translations("some sentence")
        self.assertIsInstance(literal_translations, list)
        self.assertEqual(len(literal_translations), 2)

    async def test_literal_translation_expected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 400
        requests.post.return_value.json.return_value = {
            "error_message": "Too many unique words for literal translation"
        }
        error = await self.client.fetch_literal_translations("some sentence")
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, "Too many unique words for literal translation")

    async def test_literal_translation_unexpected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 500
        requests.post.return_value.json.return_value = None
        error = await self.client.fetch_literal_translations("some sentence")
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, LITERAL_TRANSLATIONS_UNEXPECTED_ERROR)

    async def test_syntactical_analysis_happy_path(self):
        # test 200
        requests.post = Mock()
        requests.post.return_value.status_code = 200
        requests.post.return_value.json.return_value = [
            {
                "word": "some",
                "lemma": "ein",
                "morphology": "morphology",
                "dependency": "dependencies",
                "pos": "DET",
                "pos_explanation": "determiner"
            },
            {
                "word": "sentence",
                "lemma": "satz",
                "morphology": "morphology",
                "dependency": "dependencies",
                "pos": "DET",
                "pos_explanation": "determiner"
            }
        ]
        analyses = await self.client.fetch_syntactical_analysis("some sentence", "de")
        self.assertIsInstance(analyses, list)
        self.assertEqual(len(analyses), 2)

    async def test_syntactical_analysis_expected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 400
        requests.post.return_value.json.return_value = {
            "error_message": "Language not available"
        }
        error = await self.client.fetch_syntactical_analysis("some sentence", "de")
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, "Language not available")

    async def test_syntactical_analysis_unexpected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 500
        requests.post.return_value.json.return_value = None
        error = await self.client.fetch_syntactical_analysis("some sentence", "de")
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR)

    async def test_upos_explanation_happy_path(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 200
        analysis = SyntacticalAnalysis(word="word", lemma="lemma",
                                       pos="DET", morphology="morphology",
                                       dependency="dependency", pos_explanation="pos_explanation")
        requests.post.return_value.json.return_value = {
            "upos_feats": "DET",
            "explanation": "determiner",
        }
        explanation = await self.client.fetch_upos_explanation(analysis)
        self.assertIsInstance(explanation, UposExplanation)
        self.assertEqual(explanation.upos_feats, "DET")

    async def test_upos_explanation_unexpected_error(self):
        requests.post = Mock()
        requests.post.return_value.status_code = 500
        requests.post.return_value.json.return_value = None
        error = await self.client.fetch_upos_explanation(SyntacticalAnalysis(word="word", lemma="lemma",
                                                                             pos="DET", morphology="morphology",
                                                                             dependency="dependency",
                                                                             pos_explanation="pos_explanation"))
        self.assertIsInstance(error, ApplicationException)
        self.assertEqual(error.error_message, UPOS_EXPLANATIONS_UNEXPECTED_ERROR)
