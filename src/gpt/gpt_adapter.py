import json

import openai

from src.gpt.message import Message, USER, SYSTEM
from src.gpt.prompts import SYSTEM_PROMPT
from src.util.timing import timed

EMPTY_CONTEXT = [Message(role=SYSTEM, content=SYSTEM_PROMPT)]


def chat_completion(context: list[Message], prompt: str) -> dict:
    context.append(Message(role=USER, content=prompt))
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
