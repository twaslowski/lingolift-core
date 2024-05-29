import iso639
from shared.model.translation import Translation

from lingolift.generative.abstract_generator import AbstractGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.message import SYSTEM, USER, Message


class TranslationGenerator(AbstractGenerator):
    def __init__(self, llm_adapter: AbstractLLMAdapter):
        super().__init__(llm_adapter)

    def generate_translation(self, sentence: str) -> Translation:
        """
        Generate a translation for a sentence from an arbitrary language into English.
        Additionally identify the source language, represented as an ISO-3166 alpha-2 code.
        :param sentence: Sentence to translate.
        :return: Translation object
        """
        messages = [
            Message(role=SYSTEM, content=TRANSLATION_SYSTEM_PROMPT),
            Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence),
        ]
        response = self.llm_adapter.parse_response(
            self.llm_adapter.exchange(
                messages=messages, json_mode=True, model_name="gpt-4o"
            )
        )
        response["language_name"] = iso639.Language.from_part1(
            response["language_code"].lower()
        ).name
        return Translation(**response)


TRANSLATION_SYSTEM_PROMPT = """
Translate sentences from other arbitrary languages into English and identify the source language.
The source language should be returned as a ISO-3166 alpha-2 code.
Provide the response in the following JSON structure. For example:
{
  "translation": "Where is the Library?",
  "language_code": "ES"
}
"""

TRANSLATION_USER_PROMPT = """
Translate the following sentence into English:
"""
