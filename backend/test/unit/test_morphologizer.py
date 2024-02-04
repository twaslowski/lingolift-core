from unittest.mock import Mock

from shared.model.syntactical_analysis import PartOfSpeech

import generative.morphologizer as morphologizer


def test_feature_permutations_for_non_supported_pos_tag(mocker):
    analysis = Mock()
    analysis.pos = PartOfSpeech(value="ADJ", explanation="adjective")
    mocker.patch('generative.morphologizer.perform_analysis', return_value=[analysis])
    permutations = morphologizer.generate_feature_permutations("Test")
    assert permutations == []


def test_feature_permutations_for_noun(mocker):
    analysis = Mock()
    analysis.pos = PartOfSpeech(value="NOUN", explanation="noun")
    mocker.patch('generative.morphologizer.perform_analysis', return_value=[analysis])
    permutations = morphologizer.generate_feature_permutations("Test")
    # 4 cases x 2 numbers = 8 permutations
    assert len(permutations) == 8


def test_feature_permutations_for_verb(mocker):
    analysis = Mock()
    analysis.pos = PartOfSpeech(value="VERB", explanation="verb")
    mocker.patch('generative.morphologizer.perform_analysis', return_value=[analysis])
    permutations = morphologizer.generate_feature_permutations("Test")
    # 3 persons x 2 numbers = 6 permutations
    assert len(permutations) == 6
