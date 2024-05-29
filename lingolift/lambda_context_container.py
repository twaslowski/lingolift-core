import os

from lingolift.generative.literal_translation import LiteralTranslationGenerator
from lingolift.generative.morphology_generator import MorphologyGenerator
from lingolift.generative.response_suggestion import ResponseSuggestionGenerator
from lingolift.generative.translation import TranslationGenerator
from lingolift.llm.gpt_adapter import OpenAIAdapter
from lingolift.nlp.morphologizer import Morphologizer


class ContextContainer:
    """
    This class holds the context for the Lambda functions.
    Holding configuration this way allows for easier testing and dependency injection.
    Previously this would have to be done with monkey-patching or global variables; this is a cleaner solution.
    """

    gpt_adapter: OpenAIAdapter
    translation_generator: TranslationGenerator
    literal_translation_generator: LiteralTranslationGenerator
    response_suggestion_generator: ResponseSuggestionGenerator
    morphology_generator: MorphologyGenerator
    morphologizer: Morphologizer

    def __init__(self):
        self.gpt_adapter = self.initialize_gpt_adapter()
        self.translation_generator = TranslationGenerator(self.gpt_adapter)
        self.literal_translation_generator = LiteralTranslationGenerator(
            self.gpt_adapter
        )
        self.response_suggestion_generator = ResponseSuggestionGenerator(
            self.gpt_adapter
        )
        self.morphology_generator = MorphologyGenerator(self.gpt_adapter)
        self.morphologizer = Morphologizer(self.morphology_generator)

    @staticmethod
    def initialize_gpt_adapter() -> OpenAIAdapter:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        return OpenAIAdapter(openai_api_key)
