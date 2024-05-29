from test.mock_llm_adapter import MockLLMAdapter
from unittest.mock import patch

import pytest
from shared.model.inflection import Inflections
from shared.model.syntactical_analysis import (
    Morphology,
    PartOfSpeech,
    SyntacticalAnalysis,
)

from lingolift.generative import morphology_generator
from lingolift.lambda_context_container import ContextContainer


@pytest.fixture
def syntactical_analysis_noun() -> list[SyntacticalAnalysis]:
    return [
        SyntacticalAnalysis(
            word="Hund",
            pos=PartOfSpeech(value="NOUN", explanation="Noun"),
            lemma=None,
            dependency=None,
            morphology=Morphology(tags={"Gender": "Masc"}, explanation=None),
        )
    ]


@pytest.fixture
def syntactical_analysis_verb() -> list[SyntacticalAnalysis]:
    return [
        SyntacticalAnalysis(
            word="gehen",
            pos=PartOfSpeech(value="VERB", explanation="Verb"),
            lemma=None,
            dependency=None,
            morphology=Morphology(tags={"Person": "1"}, explanation=None),
        )
    ]


@pytest.fixture
def syntactical_analysis_adverb() -> list[SyntacticalAnalysis]:
    return [
        SyntacticalAnalysis(
            word="wie",
            pos=PartOfSpeech(value="ADV", explanation="Adverb"),
            lemma=None,
            dependency=None,
            morphology=None,
        )
    ]


@pytest.fixture
def mock_llm_adapter():
    return lambda: MockLLMAdapter()


@pytest.fixture
def context_container(mock_llm_adapter):
    context_container = ContextContainer(mock_llm_adapter)
    with patch.object(morphology_generator, "context_container", context_container):
        yield context_container


@pytest.mark.skip("Implementation lacking.")
def test_inflection_happy_path(morphology_generator):
    morphology = {"Number": "SING", "Person": "1"}
    inflection = morphology_generator.inflect("some-word", morphology)
    assert inflection.word == "some-word-inflection"
    assert inflection.morphology == morphology


@pytest.mark.skip(
    "Consider testing strategy: Test this as part of Lambda or in itself?"
)
def test_retrieve_inflections_for_noun(morphologizer):
    result = morphologizer.retrieve_all_inflections("Hund")

    assert isinstance(result, Inflections)
    assert result.pos.value == "NOUN"
    assert result.gender == "Masc"
    assert len(result.inflections) == 1
    assert result.inflections[0].word == "Hund"
    assert result.inflections[0].morphology == {"Case": "Nom", "Number": "Sing"}


@pytest.mark.skip(
    "Consider testing strategy: Test this as part of Lambda or in itself?"
)
def test_retrieve_inflections_for_verb(morphologizer):
    word = "gehen"
    morphology = {"Person": "1", "Number": "Sing"}
    # Given exactly one feature permutation (as opposed to the whole six for a verb)
    morphologizer._generate_feature_permutations = lambda pos_tag: [morphology]

    # When retrieving inflections for a verb
    result = morphologizer.retrieve_all_inflections(word)

    assert isinstance(result, Inflections)
    assert result.pos.value == "VERB"
    assert result.gender is None
    assert len(result.inflections) == 1


@pytest.mark.skip(
    "Consider testing strategy: Test this as part of Lambda or in itself?"
)
def test_throws_exception_for_unsupported_word_type(morphologizer):
    with pytest.raises(Exception):
        morphologizer.retrieve_all_inflections("wie")
