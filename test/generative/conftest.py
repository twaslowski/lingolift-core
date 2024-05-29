import pytest

from lingolift.generative.literal_translation import LiteralTranslationGenerator
from lingolift.generative.response_suggestion import ResponseSuggestionGenerator
from lingolift.generative.translation import TranslationGenerator
from lingolift.llm.openai_adapter import OpenAIAdapter


@pytest.fixture
def gpt_adapter() -> OpenAIAdapter:
    adapter = OpenAIAdapter(api_key="some-token", base_url="http://localhost:5002/v1/")
    return adapter


@pytest.fixture
def translation_generator(gpt_adapter):
    return TranslationGenerator(gpt_adapter)


@pytest.fixture
def literal_translation_generator(gpt_adapter):
    return LiteralTranslationGenerator(gpt_adapter)


@pytest.fixture
def response_suggestion_generator(gpt_adapter):
    return ResponseSuggestionGenerator(gpt_adapter)
