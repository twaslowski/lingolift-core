import logging
import unittest

from dacite import from_dict
from dacite.exceptions import DaciteError
from dotenv import load_dotenv

from backend.service import generate_responses, generate_translation, generate_literal_translations
from backend.test.domain.literal_translation import LiteralTranslation
from backend.test.domain.response_suggestion import ResponseSuggestion
from backend.test.domain.translation import Translation


class Benchmark(unittest.TestCase):
    BENCHMARK_SENTENCES = [
        {"sentence": "Как у тебя сегодня дела?", "language": "russian"},
        {"sentence": "Hvordan har du det i dag?", "language": "norwegian"},
        {"sentence": "Apa kabarmu hari ini?", "language": "indonesian"},
        {"sentence": "Como você está hoje?", "language": "portuguese"}
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
                parsed = from_dict(data_class=Translation, data=openai_response)
                self.assertEqual(parsed.language.lower(), sentence['language'])
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
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
                parsed = from_dict(data_class=LiteralTranslation, data=openai_response)
                self.assertEqual(len(sentence['sentence'].split()), len(parsed.words))
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
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
                openai_response = generate_responses(sentence["sentence"], expected_number_of_suggestions)
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


if __name__ == "__main__":
    unittest.main()
