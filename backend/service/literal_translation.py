import concurrent
import logging
import re

from llm.gpt_adapter import openai_exchange
from llm.message import Message, USER, SYSTEM
from llm.prompts import LITERAL_TRANSLATIONS_SYSTEM_PROMPT
from shared.model.literal_translation import LiteralTranslation

LITERAL_TRANSLATION_MAX_UNIQUE_WORDS = 15


def generate_literal_translation(sentence: str) -> list[LiteralTranslation]:
    chunks = chunk_sentence(sentence)
    if len(chunks) > LITERAL_TRANSLATION_MAX_UNIQUE_WORDS:
        logging.error(f"'{sentence}' too long for literal translation")
        raise SentenceTooLongException
    result = []
    # Create a ThreadPoolExecutor to process chunks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_literal_translation_for_chunk, sentence, chunk) for chunk in chunks]

        for future in futures:
            translation = future.result()
            for word in translation:
                result.append(word)
    return result


def generate_literal_translation_for_chunk(sentence: str, chunk: list[str]) -> list[LiteralTranslation]:
    context = [Message(role=SYSTEM, content=LITERAL_TRANSLATIONS_SYSTEM_PROMPT)]
    # not using string interpolation here, like in the other functions,
    # due to the risk of multiple threads accessing the same string object
    prompt = "Translate the word(s) '{}' in the context of the following sentence: '{}'.".format(chunk, sentence)
    context.append(Message(role=USER, content=prompt))
    # openai's json mode enforces an root level object; it doesn't appear to do a JSON list
    response = openai_exchange(context, json_mode=False)
    return [LiteralTranslation(**word) for word in response]


def chunk_sentence(sentence: str, chunk_size: int = 1) -> list[list[str]]:
    alphabetic_characters_regex = re.compile('[?!,.]')
    sentence = list(alphabetic_characters_regex.sub('', word) for word in sentence.split(' '))
    chunks = []
    for i in range(0, len(sentence), chunk_size):
        # Get a chunk of the sentence and append it to the list of chunks
        chunk = sentence[i:i + chunk_size]
        if chunk not in chunks:
            chunks.append(chunk)
    return chunks


class SentenceTooLongException(Exception):
    pass
