import unittest

from gpt.literal_translation import chunk_sentence


class LiteralTranslationTest(unittest.TestCase):

    def test_chunking_size_two(self):
        self.assertEqual(chunk_sentence("This is a test sentence"), [["This", "is"], ["a", "test"], ["sentence"]])

    def test_chunking_size_two_german(self):
        self.assertEqual(chunk_sentence("Warum ist das Huhn über die Straße gegangen?"), [["Warum", "ist"],
                                                                                          ["das", "Huhn"],
                                                                                          ["über", "die"],
                                                                                          ["Straße", "gegangen?"]])

    def test_chunking_size_one(self):
        self.assertEqual(chunk_sentence("This is a test sentence", 1),
                         [["This"], ["is"], ["a"], ["test"], ["sentence"]])
