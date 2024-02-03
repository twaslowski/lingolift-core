from nlp import universal_features


def test_tags_for_noun():
    tags = {
        "Case": "Acc",
        "Number": "Sing",
        "Gender": "Masc"
    }
    assert universal_features.convert_to_legible_tags(tags, universal_features.NOUN_FEATURE_SET) == "Accusative Singular Masculine"


def test_incomplete_tags_for_noun():
    tags = {
        "Case": "Nom",
        "Number": "Sing"
    }
    assert universal_features.convert_to_legible_tags(tags, universal_features.NOUN_FEATURE_SET) == "Nominative Singular"


def test_tags_for_verb():
    tags = {
        "Number": "Sing",
        "Person": "3",
        "Tense": "Pres"
    }
    assert universal_features.convert_to_legible_tags(tags, universal_features.VERB_FEATURE_SET) == "3rd person Singular Present tense"
