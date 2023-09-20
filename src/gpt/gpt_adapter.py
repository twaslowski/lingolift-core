import json
import logging

import openai

from gpt.context import TRANSLATION_CONTEXT, RESPONSES_CONTEXT, SYNTACTICAL_ANALYSIS_CONTEXT
from gpt.message import Message, USER
from gpt.prompts import TRANSLATION_USER_PROMPT, RESPONSES_USER_PROMPT, SYNTACTICAL_ANALYSIS_USER_PROMPT
from util.timing import timed


def _openai_exchange(messages: list[Message]) -> str:
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[message.asdict() for message in messages]
    )
    response = openai_response["choices"][0]["message"]["content"]
    logging.info(f"Received response: {response}")
    return response


@timed
def generate_translation(sentence: str) -> dict:
    context = TRANSLATION_CONTEXT
    context.append(Message(role=USER, content=TRANSLATION_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    response['original_sentence'] = sentence
    return response


@timed
def generate_syntactical_analysis(sentence: str) -> dict:
    context = SYNTACTICAL_ANALYSIS_CONTEXT
    context.append(Message(role=USER, content=SYNTACTICAL_ANALYSIS_USER_PROMPT + sentence))
    response = _parse_response(_openai_exchange(context))
    response['original_sentence'] = sentence
    return response


@timed
def generate_responses(sentence: str, number_suggestions: int = 2) -> dict:
    context = RESPONSES_CONTEXT
    prompt = RESPONSES_USER_PROMPT.format(number_suggestions, sentence)
    context.append(Message(role=USER, content=prompt))
    response = _parse_response(_openai_exchange(context))
    return response


def _parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
