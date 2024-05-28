import iso639
from shared.model.translation import Translation

from lingolift.llm.gpt_adapter import GPTAdapter
from lingolift.llm.message import SYSTEM, USER, Message


def generate_translation(sentence: str, gpt_adapter: GPTAdapter) -> Translation:
    """
    Generate a translation for a sentence from an arbitrary language into English.
    Additionally identify the source language, represented as an ISO-3166 alpha-2 code.
    :param sentence: Sentence to translate.
    :param gpt_adapter: GPTAdapter instance used to retrieve the translation.
    :return: Translation object
    """
    context = [
        Message(role=SYSTEM, content=TRANSLATION_SYSTEM_PROMPT),
        Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence),
    ]
    response = gpt_adapter.parse_response(
        gpt_adapter.openai_exchange(context, json_mode=True)
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
