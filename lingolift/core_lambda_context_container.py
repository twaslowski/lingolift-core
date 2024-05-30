from lingolift.abstract_context_container import AbstractLambdaContextContainer
from lingolift.generative.literal_translation import LiteralTranslationGenerator
from lingolift.generative.response_suggestion import ResponseSuggestionGenerator
from lingolift.generative.translation import TranslationGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter


class CoreLambdaContextContainer(AbstractLambdaContextContainer):
    """
    This class holds the context for the Lambda functions.
    Holding configuration this way allows for easier testing and dependency injection.
    Previously this would have to be done with monkey-patching or global variables; this is a cleaner solution.
    """

    translation_generator: TranslationGenerator
    literal_translation_generator: LiteralTranslationGenerator
    response_suggestion_generator: ResponseSuggestionGenerator

    def __init__(self, llm_adapter: AbstractLLMAdapter = None):
        super().__init__(llm_adapter)
        self.translation_generator = TranslationGenerator(self.llm_adapter)
        self.literal_translation_generator = LiteralTranslationGenerator(
            self.llm_adapter
        )
        self.response_suggestion_generator = ResponseSuggestionGenerator(
            self.llm_adapter
        )
