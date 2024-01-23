from nlp.universal_features import convert


def test_tags_for_noun():
    tags = ["Case=Acc", "Gender=Masc", "Number=Sing"]
    assert convert(tags) == "Accusative Singular Masculine"


def test_incomplete_tags_for_noun():
    tags = ["Case=Nom", "Number=Sing"]
    assert convert(tags) == "Nominative Singular"
