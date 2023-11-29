import logging
import os

import json5 as json
from openai import OpenAI

from backend.gpt.message import Message

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


def openai_exchange(messages: list[Message]) -> dict:
    logging.info(f"message: {messages[1].content}")
    openai_response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[message.asdict() for message in messages],
        # response_format={"type": "json_object"}
    )
    response = openai_response.choices[0].message.content
    logging.debug(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
