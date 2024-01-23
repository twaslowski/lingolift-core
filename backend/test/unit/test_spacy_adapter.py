from unittest import TestCase

from nlp.syntactical_analysis import perform_analysis, LanguageNotAvailableException


class TestSpacyAdapter(TestCase):

    def test_valid_language_code(self):
        language_code = "RU"
        sentence = "Как у тебя сегодня дела?"
        result = perform_analysis(sentence, language_code)
        self.assertIsInstance(result, list)

    def test_should_raise_exception_on_invalid_language_code(self):
        language_code = "INVALID"
        sentence = "How are you today?"
        with self.assertRaises(LanguageNotAvailableException):
            perform_analysis(sentence, language_code)

    def test_should_raise_exception_on_valid_language_code_without_model(self):
        language_code = "GR"
        sentence = "How are you today?"
        with self.assertRaises(LanguageNotAvailableException):
            perform_analysis(sentence, language_code)
