import os

from lingolift.generative.inflection_generator import InflectionGenerator
from lingolift.generative.literal_translation import LiteralTranslationGenerator
from lingolift.generative.response_suggestion import ResponseSuggestionGenerator
from lingolift.generative.translation import TranslationGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.openai_adapter import OpenAIAdapter
from lingolift.nlp.morphologizer import Morphologizer


class ContextContainer:
    """
    This class holds the context for the Lambda functions.
    Holding configuration this way allows for easier testing and dependency injection.
    Previously this would have to be done with monkey-patching or global variables; this is a cleaner solution.
    """

    llm_adapter: AbstractLLMAdapter
    translation_generator: TranslationGenerator
    literal_translation_generator: LiteralTranslationGenerator
    response_suggestion_generator: ResponseSuggestionGenerator
    morphology_generator: InflectionGenerator
    morphologizer: Morphologizer

    def __init__(self, llm_adapter: AbstractLLMAdapter = None):
        self.llm_adapter = llm_adapter or self.default_openai_adapter()
        self.translation_generator = TranslationGenerator(self.llm_adapter)
        self.literal_translation_generator = LiteralTranslationGenerator(
            self.llm_adapter
        )
        self.response_suggestion_generator = ResponseSuggestionGenerator(
            self.llm_adapter
        )
        self.morphology_generator = InflectionGenerator(self.llm_adapter)
        self.morphologizer = Morphologizer(self.morphology_generator)

    @staticmethod
    def default_openai_adapter() -> OpenAIAdapter:
        """
        Creates a default OpenAIAdapter instance.
        Notably, the "NO_KEY_PROVIDED" fallback is used to allow for testing without an API key.
        It defers the error message if the key is not provided to the OpenAIAdapter
        until when the first request is made.
        :return:
        """
        openai_api_key = os.getenv("OPENAI_API_KEY", "NO_KEY_PROVIDED")
        return OpenAIAdapter(openai_api_key)
