from lingua import LanguageDetectorBuilder, Language
from shared.exception import ApplicationException

from llm.gpt_adapter import openai_exchange
from llm.message import Message, SYSTEM, USER
import iso639

MIN_DISTANCE = 0.6
LANGUAGES = [Language.SPANISH, Language.GERMAN, Language.RUSSIAN, Language.FRENCH, Language.PORTUGUESE]
DETECTOR = (LanguageDetectorBuilder.from_languages(*LANGUAGES)
            .with_preloaded_language_models()
            .with_minimum_relative_distance(MIN_DISTANCE)
            .build())

SYSTEM_PROMPT = """Identify the language of a sentence. 
Return a JSON containing the ISO-639 Part 1 code of that language.
Your response should look like this:
{"iso_code": "DE"}
"""

USER_PROMPT = "Identify the language of the following sentence: "


class LanguageNotAvailableException(ApplicationException):
    pass


def detect_language(sentence: str) -> str:
    language = DETECTOR.detect_language_of(sentence)
    if language is None:
        raise LanguageNotAvailableException(
            f"This language was not recognized: p < {MIN_DISTANCE}. Supported languages: {LANGUAGES}")
    else:
        return str(language.iso_code_639_1).split('.')[1]


def llm_detect_language(sentence: str) -> str:
    context = [Message(role=SYSTEM, content=SYSTEM_PROMPT),
               Message(role=USER, content=USER_PROMPT + sentence)]
    response = openai_exchange(context, json_mode=True)
    try:
        language = iso639.Language.from_part1(response.get('iso_code').lower())
    except iso639.NonExistentLanguageError:
        raise LanguageNotAvailableException(
            f"The language for sentence '{sentence}' was not recognized.")
    return language.part1.upper()
