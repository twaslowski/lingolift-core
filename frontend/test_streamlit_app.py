from unittest import TestCase

from shared.model.error import ApplicationError  # type: ignore[import-untyped]
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]

from app import find_analysis, coalesce_analyses


class TestStreamlitApp(TestCase):

    def test_coalesce_analyses_happy_path(self):
        analyses = [
            SyntacticalAnalysis(word="one", morphology="some-value", lemma="some-value", dependency="some-value",
                                pos="some-value", pos_explanation="some-value"),
            SyntacticalAnalysis(word="two", morphology="some-value", lemma="some-value", dependency="some-value",
                                pos="some-value", pos_explanation="some-value")
        ]
        literal_translations = [
            LiteralTranslation(word="one", translation="uno"),
            LiteralTranslation(word="two", translation="dos"),
            LiteralTranslation(word="three", translation="tres")
        ]
        response_string = coalesce_analyses(literal_translations, analyses)
        # morphology, lemma and dependency is available for two words
        # find occurences of 'lemma' in response string
        # todo this is not really testable right now, a syntactical_analysis.stringify() method would be better

    def test_coalesce_analyses_literal_translation_error(self):
        analyses = [
            SyntacticalAnalysis(word="one", morphology="some-value", lemma="some-value", dependency="some-value",
                                pos="some-value", pos_explanation="some-value"),
            SyntacticalAnalysis(word="two", morphology="some-value", lemma="some-value", dependency="some-value",
                                pos="some-value", pos_explanation="some-value")
        ]
        literal_translations = ApplicationError(error_message="some error message")
        response_string = coalesce_analyses(literal_translations, analyses)
        # nothing except an error message gets displayed
        self.assertEqual(response_string.count("lemma"), 0)
        self.assertEqual(response_string.count("morphology"), 0)

    def test_coalesce_analyses_syntactical_analysis_error(self):
        analyses = ApplicationError(error_message="some error message")
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
            SyntacticalAnalysis(word="one", morphology="morphology", lemma="lemma", dependency="dependency",
                                pos="some-value", pos_explanation="some-value"),
            SyntacticalAnalysis(word="two", morphology="morphology", lemma="lemma", dependency="dependency",
                                pos="some-value", pos_explanation="some-value")
        ]
        self.assertEqual(find_analysis("one", analyses), analyses[0])
