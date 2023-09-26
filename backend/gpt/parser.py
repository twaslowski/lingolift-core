import logging

import json5 as json
import openai
from gpt.message import Message


def openai_exchange(messages: list[Message]) -> str:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.asdict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.info(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
