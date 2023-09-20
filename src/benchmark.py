import logging
import os
import unittest

import openai
from dacite import from_dict
from dacite.exceptions import DaciteError
from dotenv import load_dotenv

from domain.response_suggestion import ResponseSuggestion
from domain.sentence_component import SentenceComponent
from domain.translation import Translation
from gpt.gpt_adapter import generate_responses, generate_syntactical_analysis, generate_translation


class Benchmark(unittest.TestCase):
    BENCHMARK_SENTENCES = [
        "Как у тебя сегодня дела?",
        "Hvordan har du det i dag?",
        "Apa kabarmu hari ini?",
        "Como você está hoje?"
    ]

    def setUp(self) -> None:
        load_dotenv()
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def test_benchmark_translations(self):
        error_count = 0
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting response suggestions for {sentence} ...")
            try:
                openai_response = generate_translation(sentence)
                from_dict(data_class=Translation, data=openai_response)
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
        self.assertLessEqual(error_count, 1)

    def test_benchmark_responses(self):
        error_count = 0
        bad_answer_count = 0
        expected_number_of_suggestions = 2
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting translation for {sentence} ...")
            try:
                openai_response = generate_responses(sentence, expected_number_of_suggestions)
                if len(openai_response['response_suggestions']) is not expected_number_of_suggestions:
                    bad_answer_count = bad_answer_count + 1
                for response in openai_response['response_suggestions']:
                    from_dict(data_class=ResponseSuggestion, data=response)
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
        self.assertLessEqual(error_count, 1)
        self.assertLessEqual(bad_answer_count, 1)

    def test_benchmark_grammatical_analysis(self):
        error_count = 0
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting syntactical analysis for {sentence} ...")
            try:
                response = generate_syntactical_analysis(sentence)
                analysis = response['syntactical_analysis']
                for component in analysis:
                    from_dict(data_class=SentenceComponent, data=component)
            except (ValueError, KeyError):
                logging.error(f"Could not parse JSON: {response}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
        self.assertLessEqual(error_count, 1)


if __name__ == "__main__":
    unittest.main()
