from unittest.mock import Mock

from shared.model.syntactical_analysis import PartOfSpeech

import nlp.morphologizer as morphologizer


def test_feature_permutations_for_non_supported_pos_tag():
    permutations = morphologizer.generate_feature_permutations("Test")
    assert permutations == []


def test_feature_permutations_for_noun():
    permutations = morphologizer.generate_feature_permutations("NOUN")
    # 4 cases x 2 numbers = 8 permutations
    assert len(permutations) == 8


def test_feature_permutations_for_verb():
    permutations = morphologizer.generate_feature_permutations("VERB")
    # 3 persons x 2 numbers = 6 permutations
    assert len(permutations) == 6
