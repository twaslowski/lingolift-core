import pytest
from shared.exception import LanguageNotIdentifiedException

from lingolift.nlp.language_detection import detect_language


def test_detect_language_happy_path():
    sentence = "Das ist ein deutscher Satz"
    assert detect_language(sentence) == "DE"


def test_spanish_sentence():
    sentence = "esta es una frase en español"
    assert detect_language(sentence) == "ES"


def test_detect_language_that_is_not_available():
    # for speed purposes, only languages for which spacy models are available are identified
    with pytest.raises(LanguageNotIdentifiedException):
        detect_language("dette språket støttes ikke")


def test_detect_language_below_minimum_threshold():
    with pytest.raises(LanguageNotIdentifiedException):
        detect_language("this language non esta clear")


def test_detect_non_existent_language():
    with pytest.raises(LanguageNotIdentifiedException):
        detect_language("asd asoige weljfn")
