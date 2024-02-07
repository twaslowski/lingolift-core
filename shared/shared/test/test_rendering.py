import pytest

from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation
from shared.model.syntactical_analysis import SyntacticalAnalysis, PartOfSpeech
from shared.rendering import Stringifier, MarkupLanguage


@pytest.fixture
def stringifier() -> Stringifier:
    return Stringifier(MarkupLanguage.MARKDOWN)


@pytest.fixture
def pos() -> PartOfSpeech:
    return PartOfSpeech(value="VERB", explanation="Verb")


@pytest.fixture
def syntactical_analysis(pos) -> SyntacticalAnalysis:
    return SyntacticalAnalysis(
        word="one", pos=pos, lemma="uno", morphology=None, dependency="some-dep"
    )


def test_coalesce_analyses_happy_path(stringifier, syntactical_analysis):
    analyses = [syntactical_analysis]
    literal_translations = [
        LiteralTranslation(word="one", translation="uno"),
        LiteralTranslation(word="two", translation="dos"),
        LiteralTranslation(word="three", translation="tres"),
    ]
    analysis_rendered = stringifier.coalesce_analyses(literal_translations, analyses)
    lines = list(filter(lambda x: x != "", analysis_rendered.split("\n\n")))
    assert len(lines) == 4
    assert "from: " in lines[1]
    assert "refers to: " in lines[1]
    assert "from: " not in lines[2]
    assert "from: " not in lines[3]


def test_coalesce_analyses_literal_translation_error(stringifier, syntactical_analysis):
    analyses = [syntactical_analysis]
    literal_translations = ApplicationException(error_message="some error message")
    with pytest.raises(ApplicationException):
        stringifier.coalesce_analyses(literal_translations, analyses)


def test_coalesce_analyses_syntactical_analysis_error(stringifier):
    analyses = ApplicationException(error_message="some error message")
    literal_translations = [
        LiteralTranslation(word="one", translation="uno"),
        LiteralTranslation(word="two", translation="dos"),
        LiteralTranslation(word="three", translation="tres"),
    ]
    response_string = stringifier.coalesce_analyses(literal_translations, analyses)
    # translations get displayed, but no morphological analysis
    assert response_string.count("uno") == 1
    assert response_string.count("dos") == 1
    assert response_string.count("tres") == 1
    assert response_string.count("from: ") == 0
    assert response_string.count("refers to: ") == 0


def test_find_analysis(stringifier, syntactical_analysis):
    assert (
        stringifier.find_analysis("one", [syntactical_analysis]) == syntactical_analysis
    )
    assert stringifier.find_analysis("two", [syntactical_analysis]) is None
