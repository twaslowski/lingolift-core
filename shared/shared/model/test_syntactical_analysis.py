from shared.model.syntactical_analysis import Morphology


def test_happy_path():
    morph = Morphology(tags={
        "Case": "Nom",
        "Number": "Plur"
    }, explanation=None)
    assert morph.tags_to_string() == "Case=Nom|Number=Plur"


def test_empty_tags():
    morph = Morphology(tags={}, explanation=None)
    assert morph.tags_to_string() == ""


def test_explanation():
    morph = Morphology(tags={}, explanation="This is an explanation")
    assert morph.stringify_explanation() == "This is an explanation"


def test_empty_explanation_fallback():
    morph = Morphology(tags={"Case": "Nom"}, explanation=None)
    assert morph.stringify_explanation() == "Case=Nom"
