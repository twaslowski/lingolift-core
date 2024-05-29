def test_inflection_happy_path(morphology_generator, mock_llm_adapter):
    # Given a word and a corresponding set of features
    root_word = "some-word"
    morphology = {"Number": "SING", "Person": "1"}
    inflected_word = "some-word-inflection"
    mock_llm_adapter.next_response(inflected_word)

    # When inflecting the word
    inflection = morphology_generator.inflect(root_word, morphology)

    # Then the inflected word is returned
    assert inflection.word == inflected_word
    assert inflection.morphology == morphology
