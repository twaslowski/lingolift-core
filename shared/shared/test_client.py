import json
from unittest.mock import Mock

import pytest

from shared.client import Client, LITERAL_TRANSLATIONS_UNEXPECTED_ERROR, \
    SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR, UPOS_EXPLANATIONS_UNEXPECTED_ERROR
from shared.exception import ApplicationException
from shared.model.syntactical_analysis import SyntacticalAnalysis, PartOfSpeech
from shared.model.translation import Translation
from shared.model.upos_explanation import UposExplanation
from aioresponses import aioresponses

client = Client('')


# as per https://github.com/pnuckowski/aioresponses/issues/218
@pytest.fixture
def mocked():
    with aioresponses() as m:
        yield m


@pytest.mark.asyncio
async def test_translation_happy_path(mocked):
    # Create an instance of your client class
    # Mock the response from aiohttp post
    mocked.post(f"{client.host}/translation", status=200, body=json.dumps({
        "translation": "translation",
        "language_name": "german",
        "language_code": "de"
    }))

    # Call the fetch_translation method
    translation = await client.fetch_translation("some sentence")

    # Assertions
    assert isinstance(translation, Translation)
    assert translation.translation == "translation"
    assert translation.language_name == "german"
    assert translation.language_code == "de"


@pytest.mark.asyncio
async def test_literal_translation_happy_path(mocked):
    mocked.post(f"{client.host}/literal-translation", status=200, body=json.dumps([
        {
            "word": "some",
            "translation": "ein"
        },
        {
            "word": "sentence",
            "translation": "satz"
        }
    ]))
    literal_translations = await client.fetch_literal_translations("some sentence")
    assert isinstance(literal_translations, list)
    assert len(literal_translations) == 2


@pytest.mark.asyncio
async def test_literal_translation_expected_error(mocked):
    mocked.post(f"{client.host}/literal-translation", status=400, body=json.dumps({
        "error_message": "Too many words for literal translation"
    }))
    with pytest.raises(ApplicationException) as e:
        await client.fetch_literal_translations("some sentence")
        assert e.value.error_message == "Too many words for literal translation"


@pytest.mark.asyncio
async def test_syntactical_analysis_happy_path(mocked):
    mocked.post(f"{client.host}/syntactical-analysis", status=200, body=json.dumps([
        SyntacticalAnalysis(
            word="word",
            lemma="lemma",
            pos=PartOfSpeech(value="DET", explanation="determiner"),
            morphology=None,
            dependency=None
        ).model_dump(),
        SyntacticalAnalysis(
            word="word",
            lemma=None,
            pos=PartOfSpeech(value="NOUN", explanation="noun"),
            morphology=None,
            dependency="word"
        ).model_dump()]
    ))
    analyses = await client.fetch_syntactical_analysis("some sentence")
    assert isinstance(analyses, list)
    assert len(analyses) == 2
    assert isinstance(analyses[1], SyntacticalAnalysis)


@pytest.mark.asyncio
async def test_syntactical_analysis_expected_error(mocked):
    mocked.post(f"{client.host}/syntactical-analysis", status=400, body=json.dumps({
        "error_message": "Language not available"
    }))
    with pytest.raises(ApplicationException) as e:
        await client.fetch_syntactical_analysis("some sentence")
        assert e.value.error_message == "Language not available"
