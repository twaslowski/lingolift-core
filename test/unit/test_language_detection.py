import pytest
from shared.exception import LanguageNotIdentifiedException

from lingolift.nlp.lingua_language_detector import LinguaLanguageDetector


@pytest.fixture
def detector():
    return LinguaLanguageDetector()


def test_detect_language_happy_path(detector):
    sentence = "Das ist ein deutscher Satz"
    assert detector.detect_language(sentence) == "DE"


def test_spanish_sentence(detector):
    sentence = "esta es una frase en español"
    assert detector.detect_language(sentence) == "ES"


def test_detect_language_that_is_not_available(detector):
    # for speed purposes, only languages for which spacy models are available are identified
    with pytest.raises(LanguageNotIdentifiedException):
        detector.detect_language("dette språket støttes ikke")


def test_detect_language_below_minimum_threshold(detector):
    with pytest.raises(LanguageNotIdentifiedException):
        detector.detect_language("this language non esta clear")


def test_detect_non_existent_language(detector):
    with pytest.raises(LanguageNotIdentifiedException):
        detector.detect_language("asd asoige weljfn")
