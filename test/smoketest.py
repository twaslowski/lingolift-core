import os

import pytest
from shared.client import Client
from shared.exception import (
    ApplicationException,
    SentenceTooLongException,
)

client = Client(host=os.environ["API_GATEWAY_HOST"])


@pytest.mark.asyncio
async def test_translations_endpoint():
    translation = await client.fetch_translation("Donde esta la biblioteca?")
    assert translation.translation is not None
    assert translation.language_code == "ES"


@pytest.mark.asyncio
async def test_literal_translations_endpoint():
    literal_translation = await client.fetch_literal_translations(
        "Donde esta la biblioteca?"
    )
    assert len(literal_translation) > 0


@pytest.mark.asyncio
async def test_literal_translation_error_message_for_long_sentences():
    with pytest.raises(ApplicationException) as e:
        await client.fetch_literal_translations(
            "This sentence is too long for literal translation eins zwei drei vier fuenf sechs sieben acht neun zehn"
        )
    assert e.value.error_message == SentenceTooLongException().error_message


@pytest.mark.asyncio
async def test_syntactical_analysis_endpoint():
    analysis = await client.fetch_syntactical_analysis(
        sentence="Donde esta la biblioteca?", language_code="ES"
    )
    assert len(analysis) > 0


@pytest.mark.asyncio
async def test_response_suggestions_endpoint():
    suggestions = await client.fetch_response_suggestions("Donde esta la biblioteca?")
    assert len(suggestions) > 0
