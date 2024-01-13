import logging
import os

import json5 as json
from openai import OpenAI

from llm.message import Message

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


def openai_exchange(messages: list[Message], json_mode: bool = False) -> dict:
    logging.info(f"message: {messages[1].content}")
    response_format = "json_object" if json_mode else "text"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": response_format},
        messages=[message.asdict() for message in messages]
    )
    response = completion.choices[0].message.content
    logging.info(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    # sometimes, llm will hallucinate '```json' at the start of the JSON it returns .-.
    cleaned_response = gpt_response.replace('`', '').replace('json', '')
    return json.loads(cleaned_response)
