from test.integration.conftest import set_llm_response

import pytest
from shared.model.inflection import Inflections


def test_retrieve_inflections_for_noun(morphologizer, nlp_context_container):
    """
    Performs an actual analysis of the word "Hund" with spaCy; only the LLM inflection responses are mocked.
    """

    # Mock: Inflected word will be "Hund" for all feature sets for simplicity's sake
    set_llm_response(nlp_context_container, "Hund")

    # Given a noun to be inflected
    result = morphologizer.retrieve_all_inflections("Hund")

    assert isinstance(result, Inflections)
    assert result.pos.value == "NOUN"
    assert result.gender == "Masc"
    assert len(result.inflections) == 8
    assert all(inflection.word == "Hund" for inflection in result.inflections)


def test_retrieve_inflections_for_verb(morphologizer, mock_llm_adapter):
    mock_llm_adapter.next_response("gehen")

    # When retrieving inflections for a verb
    result = morphologizer.retrieve_all_inflections("gehen")

    assert isinstance(result, Inflections)
    assert result.pos.value == "VERB"
    assert result.gender is None
    assert len(result.inflections) == 6
    assert all(inflection.word == "gehen" for inflection in result.inflections)


def test_throws_exception_for_unsupported_word_type(morphologizer):
    with pytest.raises(Exception):
        morphologizer.retrieve_all_inflections("wie")
