from unittest.mock import Mock

import pytest
from shared.exception import ApplicationException
from shared.model.inflection import Inflection, Inflections
from shared.model.syntactical_analysis import PartOfSpeech

from pages.inflecTable import create_inflections_table


@pytest.fixture
def noun_inflections():
    return Inflections(
        pos=PartOfSpeech(value="NOUN", explanation="Noun"),
        gender="Masc",
        inflections=[],
    )


def test_table_should_have_three_rows_for_verb():
    inflections = Mock()
    inflections.pos = Mock()
    inflections.pos.value = "VERB"
    inflections.inflections = []
    table = create_inflections_table(inflections)
    assert len(table.split("\n")) == 5  # include markdown boilerplate header lines

    lines = table.split("\n")
    assert "ich" in lines[2] and "wir" in lines[2]
    assert "du" in lines[3] and "ihr" in lines[3]


def test_table_should_have_four_rows_for_noun(noun_inflections):
    table = create_inflections_table(noun_inflections)
    assert len(table.split("\n")) == 6  # include markdown boilerplate header lines


def test_articles_for_noun(noun_inflections):
    table = create_inflections_table(noun_inflections)
    assert len(table.split("\n")) == 6  # include markdown boilerplate header lines

    lines = table.split("\n")
    assert "der" in lines[2] and "die" in lines[2]
    assert "des" in lines[3] and "der" in lines[3]
    assert "dem" in lines[4] and "den" in lines[4]
    assert "den" in lines[5] and "die" in lines[5]


def test_application_exception_is_thrown_for_non_supported_pos():
    inflections = Mock()
    inflections.pos = Mock()
    inflections.pos.value = "ADV"
    with pytest.raises(ApplicationException):
        create_inflections_table(inflections)
