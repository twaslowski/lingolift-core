from unittest.mock import Mock

import pytest
from shared.exception import ApplicationException

from pages.inflecTable import create_inflections_table


def test_table_should_have_three_rows_for_verb():
    inflections = Mock()
    inflections.pos = Mock()
    inflections.pos.value = "VERB"
    inflections.inflections = []
    table = create_inflections_table(inflections)
    assert len(table.split("\n")) == 5  # include markdown boilerplate header lines


def test_table_should_have_four_rows_for_noun():
    inflections = Mock()
    inflections.pos = Mock()
    inflections.pos.value = "NOUN"
    inflections.inflections = []
    table = create_inflections_table(inflections)
    assert len(table.split("\n")) == 6  # include markdown boilerplate header lines


def test_application_exception_is_thrown_for_non_supported_pos():
    inflections = Mock()
    inflections.pos = Mock()
    inflections.pos.value = "ADV"
    with pytest.raises(ApplicationException):
        create_inflections_table(inflections)
