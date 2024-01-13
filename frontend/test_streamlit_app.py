from unittest import TestCase

from shared.model.error import LingoliftError
from shared.model.literal_translation import LiteralTranslation
from shared.model.syntactical_analysis import SyntacticalAnalysis
from app import find_analysis, coalesce_analyses


class TestStreamlitApp(TestCase):

    def test_coalesce_analyses_happy_path(self):
        analyses = [
            SyntacticalAnalysis(word="one", morphology="some-value", lemma="some-value", dependencies="some-value"),
            SyntacticalAnalysis(word="two", morphology="some-value", lemma="some-value", dependencies="some-value")
        ]
        literal_translations = [
            LiteralTranslation(word="one", translation="uno"),
            LiteralTranslation(word="two", translation="dos"),
            LiteralTranslation(word="three", translation="tres")
        ]
        response_string = coalesce_analyses(literal_translations, analyses)
        # morphology, lemma and dependencies is available for two words
        # find occurences of 'lemma' in response string
        self.assertEqual(response_string.count("lemma"), 2)
        self.assertEqual(response_string.count("morphology"), 2)

    def test_coalesce_analyses_literal_translation_error(self):
        analyses = [
            SyntacticalAnalysis(word="one", morphology="some-value", lemma="some-value", dependencies="some-value"),
            SyntacticalAnalysis(word="two", morphology="some-value", lemma="some-value", dependencies="some-value")
        ]
        literal_translations = LingoliftError(error_message="some error message")
        response_string = coalesce_analyses(literal_translations, analyses)
        # nothing except an error message gets displayed
        self.assertEqual(response_string.count("lemma"), 0)
        self.assertEqual(response_string.count("morphology"), 0)

    def test_coalesce_analyses_syntactical_analysis_error(self):
        analyses = LingoliftError(error_message="some error message")
        literal_translations = [
            LiteralTranslation(word="one", translation="uno"),
            LiteralTranslation(word="two", translation="dos"),
            LiteralTranslation(word="three", translation="tres")
        ]
        response_string = coalesce_analyses(literal_translations, analyses)
        # translations get displayed, but no morphological analysis
        self.assertEqual(response_string.count("uno"), 1)
        self.assertEqual(response_string.count("dos"), 1)
        self.assertEqual(response_string.count("tres"), 1)
        self.assertEqual(response_string.count("lemma"), 0)
        self.assertEqual(response_string.count("morphology"), 0)

    def test_find_analysis(self):
        analyses = [
            SyntacticalAnalysis(word="one", morphology="morphology", lemma="lemma", dependencies="dependencies"),
            SyntacticalAnalysis(word="two", morphology="morphology", lemma="lemma", dependencies="dependencies")
        ]
        self.assertEqual(find_analysis("one", analyses), analyses[0])
