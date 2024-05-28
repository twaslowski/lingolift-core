import pytest
from shared.model.inflection import Inflections
from shared.model.syntactical_analysis import (
    Morphology,
    PartOfSpeech,
    SyntacticalAnalysis,
)

import lingolift.nlp.morphologizer as morphologizer


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


@pytest.mark.skip("Implementation lacking.")
def test_inflection_happy_path(mocker):
    mocker.patch(
        "lingolift.nlp.morphologizer.openai_exchange", return_value="word_infl"
    )
    morphology = {"A": "B", "C": "D"}
    inflection = morphologizer.inflect("word", morphology)
    assert inflection.word == "word_infl"
    assert inflection.morphology == morphology


def test_retrieve_inflections_for_noun(mocker, syntactical_analysis_noun):
    mocker.patch(
        "lingolift.nlp.morphologizer.perform_analysis",
        return_value=syntactical_analysis_noun,
    )
    mocker.patch(
        "lingolift.nlp.morphologizer.generate_feature_permutations",
        return_value=[{"Case": "Nom", "Number": "Sing"}],
    )
    mocker.patch(
        "lingolift.nlp.morphologizer.inflect",
        return_value=morphologizer.Inflection(
            word="Hund", morphology={"Case": "Nom", "Number": "Sing"}
        ),
    )
    result = morphologizer.retrieve_all_inflections("Hund")

    assert isinstance(result, Inflections)
    assert result.pos.value == "NOUN"
    assert result.gender == "Masc"
    assert len(result.inflections) == 1
    assert result.inflections[0].word == "Hund"
    assert result.inflections[0].morphology == {"Case": "Nom", "Number": "Sing"}


def test_retrieve_inflections_for_verb(mocker, syntactical_analysis_verb):
    mocker.patch(
        "lingolift.nlp.morphologizer.perform_analysis",
        return_value=syntactical_analysis_verb,
    )
    mocker.patch(
        "lingolift.nlp.morphologizer.generate_feature_permutations",
        return_value=[{"Person": "1", "Number": "Sing"}],
    )
    mocker.patch(
        "lingolift.nlp.morphologizer.inflect",
        return_value=morphologizer.Inflection(
            word="gehe", morphology={"Person": "1", "Number": "Sing"}
        ),
    )
    result = morphologizer.retrieve_all_inflections("gehen")

    assert isinstance(result, Inflections)
    assert result.pos.value == "VERB"
    assert result.gender is None
    assert len(result.inflections) == 1


def test_throws_exception_for_unsupported_word_type(
    mocker, syntactical_analysis_adverb
):
    mocker.patch(
        "lingolift.nlp.morphologizer.perform_analysis",
        return_value=syntactical_analysis_adverb,
    )
    with pytest.raises(Exception):
        morphologizer.retrieve_all_inflections("wie")
