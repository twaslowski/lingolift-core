from shared.model.upos_explanation import UposExplanation

from nlp.syntactical_analysis import perform_analysis


def test_happy_path(mocker):
    # Perform one comprehensive test, because analyses are quite slow.
    sentence = "Satzzeichen werden nicht gezählt."
    result = list(perform_analysis(sentence))

    # ensure punctuation tokens are omitted from the analysis
    assert len(result) == 4

    assert result[0].pos.value == "NOUN"
    assert result[1].pos.value == "AUX"
    assert result[1].morphology.explanation == "3rd person Plural Present tense"
    assert result[3].pos.value == "VERB"

