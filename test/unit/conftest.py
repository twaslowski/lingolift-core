from test.mock_llm_adapter import MockLLMAdapter

import pytest

from lingolift.generative.inflection_generator import InflectionGenerator
from lingolift.generative.literal_translation import LiteralTranslationGenerator
from lingolift.generative.response_suggestion import ResponseSuggestionGenerator
from lingolift.generative.translation import TranslationGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.nlp.morphologizer import Morphologizer


@pytest.fixture
def mock_llm_adapter() -> AbstractLLMAdapter:
    return MockLLMAdapter()


@pytest.fixture
def translation_generator(mock_llm_adapter) -> TranslationGenerator:
    return TranslationGenerator(mock_llm_adapter)


@pytest.fixture
def literal_translation_generator(mock_llm_adapter) -> LiteralTranslationGenerator:
    return LiteralTranslationGenerator(mock_llm_adapter)


@pytest.fixture
def response_suggestion_generator(mock_llm_adapter) -> ResponseSuggestionGenerator:
    return ResponseSuggestionGenerator(mock_llm_adapter)


@pytest.fixture
def morphology_generator(mock_llm_adapter) -> InflectionGenerator:
    return InflectionGenerator(mock_llm_adapter)


@pytest.fixture
def morphologizer(morphology_generator) -> Morphologizer:
    return Morphologizer(morphology_generator)
