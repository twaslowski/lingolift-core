from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

import pytest
import requests  # type: ignore[import-untyped]

from shared.client import Client, LITERAL_TRANSLATIONS_UNEXPECTED_ERROR, \
    SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR, UPOS_EXPLANATIONS_UNEXPECTED_ERROR
from shared.exception import ApplicationException
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation
from shared.model.upos_explanation import UposExplanation


# todo fix tests
# this is actually not terribly easy to fix; a lot of threads recommend asynctest.CoroutineMock(),
# but CoroutineMock appears to use the deprecated @asyncio.coroutine decorator,
# which means it's not compatible with Python 3.12. I really don't want to downgrade my Python version to 3.11 just
# for this. Not to mention that would break a bunch of other things because of the way I do typing.
@pytest.mark.asyncio
async def test_translation_happy_path(mocker):
    # Create an instance of your client class
    client = Client()

    # Mock the response from aiohttp post
    mock_response = mocker.MagicMock()
    mock_response.status = 200
    mock_response.json = mocker.AsyncMock(return_value={
        "translation": "translation",
        "language_name": "german",
        "language_code": "de"
    })

    # Use mocker to patch aiohttp.ClientSession.post
    mocker.patch('aiohttp.ClientSession.post',
                 return_value=mocker.Mock(__aenter__=CoroutineMock(return_value=mock_response)))

    # Call the fetch_translation method
    translation = await client.fetch_translation("some sentence")

    # Assertions
    assert isinstance(translation, Translation)
    assert translation.translation == "translation"
    assert translation.language_name == "german"
    assert translation.language_code == "de"


async def test_translation_unexpected_error(self):
    requests.post = Mock()
    requests.post.return_value.status_code = 500
    requests.post.return_value.json.return_value = None
    with self.assertRaises(ApplicationException):
        await self.client.fetch_translation("some sentence")


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
    with self.assertRaises(ApplicationException):
        await self.client.fetch_literal_translations("some sentence")


async def test_literal_translation_unexpected_error(self):
    requests.post = Mock()
    requests.post.return_value.status_code = 500
    requests.post.return_value.json.return_value = None
    with self.assertRaises(ApplicationException) as e:
        await self.client.fetch_literal_translations("some sentence")
        self.assertEqual(e.exception.error_message, LITERAL_TRANSLATIONS_UNEXPECTED_ERROR)


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
    with self.assertRaises(ApplicationException) as e:
        await self.client.fetch_syntactical_analysis("some sentence", "de")
        self.assertEqual(e.exception.error_message, "Language not available")


async def test_syntactical_analysis_unexpected_error(self):
    requests.post = Mock()
    requests.post.return_value.status_code = 500
    requests.post.return_value.json.return_value = None
    with self.assertRaises(ApplicationException) as e:
        await self.client.fetch_syntactical_analysis("some sentence", "de")
        self.assertEqual(e.exception.error_message, SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR)


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
    with self.assertRaises(ApplicationException) as e:
        await self.client.fetch_upos_explanation(SyntacticalAnalysis(word="word", lemma="lemma",
                                                                     pos="DET", morphology="morphology",
                                                                     dependency="dependency",
                                                                     pos_explanation="pos_explanation"))
        self.assertEqual(e.exception.error_message, UPOS_EXPLANATIONS_UNEXPECTED_ERROR)
