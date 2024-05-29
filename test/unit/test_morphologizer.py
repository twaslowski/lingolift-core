def test_feature_permutations_for_non_supported_pos_tag(morphologizer):
    permutations = morphologizer._generate_feature_permutations("non-supported-pos-tag")
    assert permutations == []


def test_feature_permutations_for_noun(morphologizer):
    permutations = morphologizer._generate_feature_permutations("NOUN")
    # 4 cases x 2 numbers = 8 permutations
    assert len(permutations) == 8


def test_feature_permutations_for_verb(morphologizer):
    permutations = morphologizer._generate_feature_permutations("VERB")
    # 3 persons x 2 numbers = 6 permutations
    assert len(permutations) == 6
