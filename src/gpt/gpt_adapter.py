import json
import logging

import openai

from src.gpt.message import Message, USER
from src.util.timing import timed


def chat_completion(context: list[Message], prompt: str) -> dict:
    context.append(Message(role=USER, content=prompt))
    logging.info("")
    response = _get_response(context)
    return _parse_response(response)


@timed
def _get_response(messages: list[Message]):
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message.asdict() for message in messages]
    )
    return openai_response["choices"][0]["message"]["content"]


def _parse_response(gpt_response: str) -> dict:
    try:
        response_json = json.loads(gpt_response)
        return response_json
    except ValueError as e:
        print(f"Response could not be parsed to JSON: {gpt_response}\n Error: {e}")
