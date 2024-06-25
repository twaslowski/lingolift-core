from lingolift.nlp.syntactical_analysis import perform_analysis


def test_happy_path(monkeypatch):
    # Define the environment variable to load the correct spaCy model.
    monkeypatch.setenv("SPACY_MODEL", "de_core_news_sm")

    # Perform one comprehensive test, because analyses are quite slow.
    sentence = "Satzzeichen werden nicht gezählt."
    result = list(perform_analysis(sentence))

    # ensure punctuation tokens are omitted from the analysis
    assert len(result) == 4

    assert result[0].upos.value == "noun"
    assert result[1].upos.value == "auxiliary verb"
    assert result[1].feature_set.__str__() == "Third person Plural Present tense"
    assert result[3].upos.value == "verb"
