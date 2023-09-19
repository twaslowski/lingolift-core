import json
import logging

import openai

from src.gpt.context import TRANSLATION_CONTEXT, RESPONSES_CONTEXT, SYNTACTICAL_ANALYSIS_CONTEXT
from src.gpt.message import Message, USER
from src.gpt.prompts import TRANSLATION_USER_PROMPT, RESPONSES_USER_PROMPT, SYNTACTICAL_ANALYSIS_USER_PROMPT
from src.util.timing import timed


def _openai_exchange(messages: list[Message]) -> str:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[message.asdict() for message in messages]
    )
    return openai_response["choices"][0]["message"]["content"]


@timed
def generate_translation(sentence: str) -> dict:
    context = TRANSLATION_CONTEXT
    context.append(Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    logging.info(f"Received OpenAI response: {response}")
    response['original_sentence'] = sentence
    return response


@timed
def generate_syntactical_analysis(sentence: str) -> dict:
    context = SYNTACTICAL_ANALYSIS_CONTEXT
    context.append(Message(role=USER, content=SYNTACTICAL_ANALYSIS_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    return response


@timed
def generate_responses(sentence: str) -> dict:
    context = RESPONSES_CONTEXT
    context.append(Message(role=USER, content=RESPONSES_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    return response


def _parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
