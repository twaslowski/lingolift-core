import logging
import os
import unittest

import openai
from dacite import from_dict
from dacite.exceptions import DaciteError
from dotenv import load_dotenv

from src.domain.response import Response
from src.gpt.gpt_adapter import _get_response, _parse_response
from src.gpt.message import SYSTEM, Message, USER
from src.gpt.prompts import SYSTEM_PROMPT


class Benchmark(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def test_valid_json_is_returned_for_short_prompt(self):
        error_count = 0
        benchmark_sentences = [
            "Как у тебя сегодня дела?",
            "Hvordan har du det i dag?",
            "Apa kabarmu hari ini?",
            "Como você está hoje?"
        ]
        for sentence in benchmark_sentences:
            logging.info(f"Testing for {sentence} ...")
            context = [Message(role=SYSTEM, content=SYSTEM_PROMPT), Message(role=USER, content=sentence)]
            response = _get_response(context)
            try:
                parsed = _parse_response(response)
                from_dict(data_class=Response, data=parsed)
                logging.info(parsed)
            except (ValueError, DaciteError) as e:
                logging.error(e)
                error_count = error_count + 1
                continue
        self.assertLessEqual(error_count, 1)


if __name__ == "__main__":
    unittest.main()
