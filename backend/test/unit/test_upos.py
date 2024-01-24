from unittest.mock import Mock

from nlp.syntactical_analysis import extract_relevant_tags


def test_upos_extraction_determiner():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'DET'
    relevant_tags = extract_relevant_tags(token)
    assert len(relevant_tags) == 1

def test_upos_extraction_verb():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'VERB'
    relevant_tags = extract_relevant_tags(token)
    assert len(relevant_tags) == 3


def test_upos_extraction_misc():
    token = Mock()
    token.morph = 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin'
    token.pos_ = 'NON_RELEVANT'
    relevant_tags = extract_relevant_tags(token)
    assert len(relevant_tags) == 0