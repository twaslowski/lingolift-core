from unittest.mock import Mock

import pytest

from nlp.syntactical_analysis import pos_tags_to_dict


@pytest.mark.skip(reason="refactoring, may not be needed")
def test_upos_extraction_determiner():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'DET'
    relevant_tags = pos_tags_to_dict(token)
    assert len(relevant_tags) == 1


@pytest.mark.skip(reason="refactoring, may not be needed")
def test_upos_extraction_verb():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'VERB'
    relevant_tags = pos_tags_to_dict(token)
    assert len(relevant_tags) == 3


@pytest.mark.skip(reason="refactoring, may not be needed")
def test_upos_extraction_misc():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'NON_RELEVANT'
    relevant_tags = pos_tags_to_dict(token)
    assert len(relevant_tags) == 0
