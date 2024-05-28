from unittest.mock import Mock

import pytest
from lingolift.nlp.syntactical_analysis import pos_tags_to_dict


def test_feature_extraction_to_dict():
    token = Mock()
    token.morph = "Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin"
    relevant_tags = pos_tags_to_dict(token)
    assert "Mood" in relevant_tags
    assert "Number" in relevant_tags
    assert "Person" in relevant_tags
    assert "Tense" in relevant_tags
    assert "VerbForm" in relevant_tags
    assert relevant_tags["Mood"] == "Ind"
    assert relevant_tags["Number"] == "Sing"
    assert relevant_tags["Person"] == "3"
    assert relevant_tags["Tense"] == "Pres"
    assert relevant_tags["VerbForm"] == "Fin"


def test_empty_feature_extraction():
    token = Mock()
    token.morph = ""
    relevant_tags = pos_tags_to_dict(token)
    assert relevant_tags == {}
