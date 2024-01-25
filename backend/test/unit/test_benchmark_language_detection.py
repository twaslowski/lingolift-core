from nlp.language_detection import detect_language


# todo this process needs to become more reliable
def test_should_recognize_short_sentence():
    assert detect_language("Das ist ein kurzer Satz") == "DE"
    assert detect_language("Das ist ein Test") == "DE"
