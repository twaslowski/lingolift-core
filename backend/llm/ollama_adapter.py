import logging

import requests

from backend.llm.message import Message, USER
from backend.util.timing import timed

OLLAMA_ENDPOINT = "http://localhost:11434"


@timed
def ollama_exchange(messages: list[Message], json_mode: bool = False):
    mode = "json" if json_mode else None
    response = requests.post(f"http://localhost:11434/api/chat", json={
        "model": "llama2-uncensored:7b",
        "messages": [message.asdict() for message in messages],
        "stream": False,
        "mode": mode
    }).json()
    time_elapsed = response['total_duration'] / 10e9
    return response


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print(ollama_exchange([Message(USER, "how are you doing? respond with a valid json")], True))
