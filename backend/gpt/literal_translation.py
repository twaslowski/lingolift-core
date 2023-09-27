import concurrent
import logging

from backend.gpt.gpt_adapter import openai_exchange
from backend.gpt.message import Message, USER, SYSTEM
from backend.gpt.prompts import LITERAL_TRANSLATIONS_SYSTEM_PROMPT


def generate_literal_translation(sentence: str) -> dict:
    chunks = chunk_sentence(sentence)
    result = {"words": []}
    # Create a ThreadPoolExecutor to process chunks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_literal_translation_for_chunk, sentence, chunk) for chunk in chunks]

        for future in concurrent.futures.as_completed(futures):
            translation = future.result()
            for word in translation:
                result["words"].append(word)

    return result


def generate_literal_translation_for_chunk(sentence: str, chunk: list[str]) -> dict:
    logging.info(f"Sending sentence {sentence}, chunk {chunk} to gpt3")
    context = [Message(role=SYSTEM, content=LITERAL_TRANSLATIONS_SYSTEM_PROMPT)]
    prompt = "Translate the word(s) '{}' in the context of the following sentence: '{}'.".format(chunk, sentence)
    context.append(Message(role=USER, content=prompt))
    response = openai_exchange(context)
    return response


def chunk_sentence(sentence: str, chunk_size: int = 2) -> list[list[str]]:
    sentence = list(sentence.split(' '))
    chunks = []
    for i in range(0, len(sentence), chunk_size):
        # Get a chunk of the sentence and append it to the list of chunks
        chunk = sentence[i:i + chunk_size]
        chunks.append(chunk)
    return chunks


if __name__ == '__main__':
    generate_literal_translation("das hier ist ein satz zum testen")
