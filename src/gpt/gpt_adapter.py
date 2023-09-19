import json

import openai

from src.gpt.message import Message, USER, SYSTEM
from src.gpt.prompts import SYSTEM_PROMPT, TRANSLATION_CONTEXT, TRANSLATION_PROMPT
from src.util.timing import timed

EMPTY_CONTEXT = [Message(role=SYSTEM, content=SYSTEM_PROMPT)]
TRANSLATION_CONTEXT = [Message(role=SYSTEM, content=TRANSLATION_CONTEXT)]


@timed
def _openai_exchange(messages: list[Message]):
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[message.asdict() for message in messages]
    )
    return openai_response["choices"][0]["message"]["content"]


@timed
def get_summary(sentence: str) -> dict:
    context = TRANSLATION_CONTEXT
    context.append(Message(role=USER, content=TRANSLATION_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    response['original_sentence'] = sentence
    return response


def _parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
