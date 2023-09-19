import json

import openai

from src.gpt.message import Message, USER, SYSTEM
from src.gpt.prompts import SYSTEM_PROMPT, TRANSLATION_SYSTEM_PROMPT, TRANSLATION_USER_PROMPT, RESPONSES_SYSTEM_PROMPT, \
    RESPONSES_USER_PROMPT
from src.util.timing import timed

EMPTY_CONTEXT = [Message(role=SYSTEM, content=SYSTEM_PROMPT)]
TRANSLATION_CONTEXT = [Message(role=SYSTEM, content=TRANSLATION_SYSTEM_PROMPT)]
RESPONSES_CONTEXT = [Message(role=SYSTEM, content=RESPONSES_SYSTEM_PROMPT)]


def _openai_exchange(messages: list[Message]):
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[message.asdict() for message in messages]
    )
    return openai_response["choices"][0]["message"]["content"]


@timed
def generate_translation(sentence: str) -> dict:
    context = TRANSLATION_SYSTEM_PROMPT
    context.append(Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    response['original_sentence'] = sentence
    return response


@timed
def generate_breakdown(sentence: str) -> dict:
    pass


@timed
def generate_responses(sentence: str) -> dict:
    context = RESPONSES_CONTEXT
    context.append(Message(role=USER, content=RESPONSES_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    return response


def _parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
