import logging
import unittest

from dotenv import load_dotenv
from pydantic import ValidationError
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

from service.generate import generate_response_suggestions, generate_translation, generate_literal_translations


class Benchmark(unittest.TestCase):
    BENCHMARK_SENTENCES = [
        {"sentence": "Как у тебя сегодня дела?", "language": "RU"},
        {"sentence": "Wie viel kostet ein Bier?‘", "language": "DE"},
        {"sentence": "donde esta la biblioteca?", "language": "ES"},
        {"sentence": "Como você está hoje?", "language": "PT"},
        {"sentence": "c'est la vie", "language": "FR"}
    ]

    def setUp(self) -> None:
        load_dotenv()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def test_benchmark_translations(self):
        error_count = 0
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting translations for {sentence} ...")
            try:
                openai_response = generate_translation(sentence["sentence"])
                self.assertEqual(openai_response.language_code, sentence['language'])
            except ValidationError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
                continue
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except AssertionError as ae:
                logging.error(f"Error with assertion: {ae}")
                error_count = error_count + 1
                continue
        self.assertLessEqual(error_count, 1)

    def test_benchmark_literal_translations(self):
        error_count = 0
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting literal translations for {sentence} ...")
            try:
                openai_response = generate_literal_translations(sentence["sentence"])
                self.assertEqual(len(sentence['sentence'].split()), len(openai_response))
            except ValidationError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
                continue
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except AssertionError as ae:
                logging.error(f"Error with assertion: {ae}")
                error_count = error_count + 1
                continue
        self.assertLessEqual(error_count, 1)

    def test_benchmark_responses(self):
        error_count = 0
        bad_answer_count = 0
        expected_number_of_suggestions = 2
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting response suggestions for {sentence} ...")
            try:
                openai_response = generate_response_suggestions(sentence["sentence"], expected_number_of_suggestions)
                if len(openai_response) is not expected_number_of_suggestions:
                    bad_answer_count = bad_answer_count + 1
            except ValidationError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
        self.assertLessEqual(error_count, 1)
        self.assertLessEqual(bad_answer_count, 1)


if __name__ == "__main__":
    unittest.main()
