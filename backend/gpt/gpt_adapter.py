import logging

import json5 as json
import openai

from backend.gpt.message import Message


def openai_exchange(messages: list[Message]) -> dict:
    logging.info(f"message: {messages[1].content}")
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.asdict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.debug(f"Received response: {response}")
    return response


def parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
