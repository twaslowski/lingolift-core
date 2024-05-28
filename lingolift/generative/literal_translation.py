import logging
import re
from concurrent.futures import ThreadPoolExecutor

from shared.exception import SentenceTooLongException
from shared.model.literal_translation import LiteralTranslation

from lingolift.generative.abstract_generator import AbstractGenerator
from lingolift.llm.gpt_adapter import GPTAdapter
from lingolift.llm.message import SYSTEM, USER, Message

LITERAL_TRANSLATION_MAX_UNIQUE_WORDS = 15


class LiteralTranslationGenerator(AbstractGenerator):
    def __init__(self, gpt_adapter: GPTAdapter):
        super().__init__(gpt_adapter)

    def generate_literal_translation(self, sentence: str) -> list[LiteralTranslation]:
        """
        Translates all words of the sentence in parallel by sending them to the inference engine.
        Notably, this is done via an LLM instead of e.g. DeepL for disambiguation purposes. Asking the LLM to specifically
        translate words in the context of a sentence ensures that ambiguous words will be translated as intended.
        Uses a ThreadPoolExecutor() to perform requests in parallel as to speed up the generation of translations as much
        as possible.
        In order to
        :param sentence:
        :return:
        """
        chunks = self._chunk_sentence(sentence)
        if len(chunks) > LITERAL_TRANSLATION_MAX_UNIQUE_WORDS:
            logging.error(f"'{sentence}' too long for literal translation")
            raise SentenceTooLongException()
        result = []
        # Create a ThreadPoolExecutor to process chunks concurrently
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self._generate_literal_translation_for_chunk, sentence, chunk
                )
                for chunk in chunks
            ]

            for future in futures:
                translation = future.result()
                for word in translation:
                    result.append(word)
        return result

    def _generate_literal_translation_for_chunk(
        self, sentence: str, chunk: list[str]
    ) -> list[LiteralTranslation]:
        """
        Submits a given chunk – a list of words – to the inference engine for translation.
        :param sentence: The base sentence containing the translated words
        :param chunk: words to be translated
        :return:
        """
        context = [Message(role=SYSTEM, content=LITERAL_TRANSLATIONS_SYSTEM_PROMPT)]
        # Not using string interpolation here, like in the other functions, due to multithreading issues
        prompt = "Translate the word(s) '{}' in the context of the following sentence: '{}'.".format(
            chunk, sentence
        )
        context.append(Message(role=USER, content=prompt))
        # OpenAI's JSON mode enforces a root level object
        # I want to return a list here, therefore JSON mode doesn't work
        response = self.gpt_adapter.parse_response(
            self.gpt_adapter.openai_exchange(context, json_mode=False)
        )

        return [LiteralTranslation(**word) for word in response]

    @staticmethod
    def _chunk_sentence(sentence: str, chunk_size: int = 1) -> list[list[str]]:
        """
        Takes a sentence and converts it into chunks of words that can be submitted to the OpenAI API.
        Typing notes: For some reason, mypy struggles to understand what I'm doing here, hence the ignores.
        Refer to the unit tests to verify that this function behaves as intended.
        :param sentence: Sentence to be translated.
        :param chunk_size: Defaults to 1, as this turns out to be the most time- and resource-efficient solution.
        Could probably be hardcoded to 1 entirely.
        :return:
        """
        alphabetic_characters_regex = re.compile("[?!,.]")
        sentence = list(alphabetic_characters_regex.sub("", word) for word in sentence.split(" "))  # type: ignore
        chunks = []
        for i in range(0, len(sentence), chunk_size):
            # Get a chunk of the sentence and append it to the list of chunks
            chunk = sentence[i : i + chunk_size]
            if chunk not in chunks:
                chunks.append(chunk)
        return chunks  # type: ignore


LITERAL_TRANSLATIONS_SYSTEM_PROMPT = """
Provide literal translations for words in the context of a sentence.
You will receive a JSON with a sentence and one or multiple words, and provide a response in the following structure:
[{
      "word": "PLACEHOLDER_WORD",
      "translation": "PLACEHOLDER_LITERAL_TRANSLATION"
}]
"""
