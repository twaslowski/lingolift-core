import unittest
from backend.llm import gpt_adapter


class TestGptAdapter(unittest.TestCase):

    def test_parse_gpt_response(self):
        happy_path = """{
            "literal_translation": "Hello! How are you?",
            "words": [
                {
                    "word": "Moin!",
                    "translation": "Hello!"
                },
                {
                    "word": "Wie",
                    "translation": "How"
                },
                {
                    "word": "geht",
                    "translation": "goes"
                },
                {
                    "word": "es",
                    "translation": "it"
                },
                {
                    "word": "dir",
                    "translation": "you"
                }
            ]
        }"""
        gpt_adapter.parse_response(happy_path)
        self.assertTrue(True)  # when getting here the previous function has not thrown an exception

    def test_parser_manages_trailing_commas(self):
        happy_path = """{
            "literal_translation": "Hello! How are you?",
            "words": [
                {
                    "word": "Moin!",
                    "translation": "Hello!",
                },
                {
                    "word": "Wie",
                    "translation": "How",
                },
                {
                    "word": "geht",
                    "translation": "goes",
                },
                {
                    "word": "es",
                    "translation": "it",
                },
                {
                    "word": "dir",
                    "translation": "you",
                }
            ]
        }"""
        gpt_adapter.parse_response(happy_path)
        self.assertTrue(True)  # when getting here the previous function has not thrown an exception
