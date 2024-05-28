import pytest
from shared.exception import SentenceTooLongException

from lingolift.generative.literal_translation import LiteralTranslationGenerator


@pytest.fixture
def literal_translation_generator(gpt_adapter):
    return LiteralTranslationGenerator(gpt_adapter)


def test_chunking_size_two(literal_translation_generator):
    assert literal_translation_generator._chunk_sentence(
        "This is a test sentence", chunk_size=2
    ) == [["This", "is"], ["a", "test"], ["sentence"]]


def test_chunking_size_two_german(literal_translation_generator):
    assert literal_translation_generator._chunk_sentence(
        "Warum ist das Huhn über die Straße gegangen?", chunk_size=2
    ) == [["Warum", "ist"], ["das", "Huhn"], ["über", "die"], ["Straße", "gegangen"]]


def test_chunking_size_one(literal_translation_generator):
    assert literal_translation_generator._chunk_sentence(
        "This is a test sentence", chunk_size=1
    ) == [["This"], ["is"], ["a"], ["test"], ["sentence"]]


def test_chunking_with_cyrillic(literal_translation_generator):
    assert literal_translation_generator._chunk_sentence(
        "Как у тебя сегодня дела?"
    ) == [["Как"], ["у"], ["тебя"], ["сегодня"], ["дела"]]


def test_word_should_not_be_translated_more_than_once(literal_translation_generator):
    assert literal_translation_generator._chunk_sentence("word word other word") == [
        ["word"],
        ["other"],
    ]


def test_sentence_above_threshold_size_should_raise_exception(
    literal_translation_generator,
):
    with pytest.raises(SentenceTooLongException):
        literal_translation_generator.generate_literal_translation(
            "this sentence is too long because it "
            "contains too many unique words a b c d e gf "
        )
