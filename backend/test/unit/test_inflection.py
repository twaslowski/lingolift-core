import nlp.morphologizer as morphologizer


def test_inflection_happy_path(mocker):
    mocker.patch('nlp.morphologizer.openai_exchange', return_value="word_infl")
    morphology = {
        "A": "B",
        "C": "D"
    }
    inflection = morphologizer.inflect("word", morphology)
    assert inflection.word == "word_infl"
    assert inflection.morphology == morphology
