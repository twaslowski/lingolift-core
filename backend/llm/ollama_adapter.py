import json
import logging

import requests  # type: ignore[import-untyped]

from llm.message import Message, USER
from util.timing import timed

OLLAMA_ENDPOINT = "http://localhost:11434"


@timed
def ollama_exchange(messages: list[Message], json_mode: bool = False):
    mode = "json" if json_mode else None
    response = requests.post(f"http://localhost:11434/api/chat", json={
        "model": "llama2:13b",
        "messages": [message.asdict() for message in messages],
        "stream": False,
        "mode": mode
    }).json()
    raw_response = response['message']['content']
    logging.info(f"Received ollama response: {raw_response}")
    return parse_json(raw_response)


def parse_json(response: str) -> dict:
    start_json_index = response.find('{')
    end_json_index = response.find('}')
    json_truncated = response[start_json_index:end_json_index + 1]
    logging.info(f"Truncated JSON: {json_truncated}")
    return json.loads(json_truncated)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print(ollama_exchange([Message(USER, "how are you doing? respond with a valid json")], json_mode=True))
