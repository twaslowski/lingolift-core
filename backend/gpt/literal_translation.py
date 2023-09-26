from gpt.context import LITERAL_TRANSLATIONS_CONTEXT
from gpt.prompts import LITERAL_TRANSLATIONS_USER_PROMPT
from gpt.message import Message, USER
from gpt.parser import openai_exchange
import concurrent


def generate_literal_translation(sentence: str) -> dict:
    chunks = chunk_sentence(sentence)
    result = {"words": []}
    # Create a ThreadPoolExecutor to process chunks concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use a list to keep track of the futures
        futures = []

        for chunk in chunks:
            # Submit each chunk for processing and store the future
            future = executor.submit(generate_literal_translation_for_chunk, sentence, chunk)
            futures.append(future)

        # Retrieve the results from the futures as they complete
        for future in concurrent.futures.as_completed(futures):
            translation = future.result()
            for word in translation:
                result["words"].append(word)

    print(result)
    return result

def generate_literal_translation_for_chunk(sentence: str, chunk: list[str]) -> dict:
    context = LITERAL_TRANSLATIONS_CONTEXT
    prompt = LITERAL_TRANSLATIONS_USER_PROMPT.format(chunk, sentence)
    context.append(Message(role=USER, content=prompt))
    return openai_exchange(context)


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