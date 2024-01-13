import unittest

from service.literal_translation import chunk_sentence, SentenceTooLongException, generate_literal_translation


class LiteralTranslationTest(unittest.TestCase):

    def test_chunking_size_two(self):
        self.assertEqual(chunk_sentence("This is a test sentence", chunk_size=2),
                         [["This", "is"], ["a", "test"], ["sentence"]])

    def test_chunking_size_two_german(self):
        self.assertEqual(chunk_sentence("Warum ist das Huhn über die Straße gegangen?", chunk_size=2),
                         [["Warum", "ist"],
                          ["das", "Huhn"],
                          ["über", "die"],
                          ["Straße", "gegangen"]])

    def test_chunking_size_one(self):
        self.assertEqual(chunk_sentence("This is a test sentence", ),
                         [["This"], ["is"], ["a"], ["test"], ["sentence"]])

    def test_chunking_with_cyrillic(self):
        self.assertEqual(chunk_sentence('Как у тебя сегодня дела?'), [['Как'], ['у'], ['тебя'], ['сегодня'], ['дела']])

    def test_word_should_not_be_translated_more_than_once(self):
        self.assertEqual(chunk_sentence("word word other word"), [['word'], ['other']])

    def test_sentence_above_threshold_size_should_raise_exception(self):
        with self.assertRaises(SentenceTooLongException):
            generate_literal_translation("this sentence is too long because it "
                                         "contains too many unique words a b c d e gf ")
