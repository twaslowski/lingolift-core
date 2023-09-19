import logging
import os
import unittest

import openai
from dacite import from_dict
from dacite.exceptions import DaciteError
from dotenv import load_dotenv

from src.domain.response import Response
from src.domain.translation import Translation
from src.gpt.gpt_adapter import _openai_exchange, _parse_response, get_summary
from src.gpt.message import SYSTEM, Message, USER
from src.gpt.prompts import SYSTEM_PROMPT


class Benchmark(unittest.TestCase):
    BENCHMARK_SENTENCES = [
        "Как у тебя сегодня дела?"
        "Hvordan har du det i dag?",
        "Apa kabarmu hari ini?",
        "Como você está hoje?"
    ]

    def setUp(self) -> None:
        load_dotenv()
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def test_benchmark_summary(self):
        error_count = 0
        for sentence in self.BENCHMARK_SENTENCES:
            logging.info(f"Getting translation for {sentence} ...")
            try:
                response = get_summary(sentence)
                from_dict(data_class=Translation, data=response)
            except ValueError as ve:
                logging.error(f"Could not parse JSON: {ve}")
                error_count = error_count + 1
                continue
            except DaciteError as de:
                logging.error(f"Error serializing JSON to dataclass: {de}")
                error_count = error_count + 1
        self.assertLessEqual(error_count, 1)


if __name__ == "__main__":
    unittest.main()
