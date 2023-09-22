import json
import logging

import openai
from gpt.context import *
from gpt.message import Message, USER
from gpt.prompts import *
from util.timing import timed


def _openai_exchange(messages: list[Message]) -> str:
    openai_response = openai.ChatCompletion.create(
        model="gpt-4",
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


@timed
def generate_word_inflections(language: str, sentence_context: str, word: str) -> dict:
    context = WORD_INFLECTIONS_CONTEXT
    prompt = WORD_INFLECTIONS_USER_PROMPT.format(sentence_context, word)
    context.append(Message(role=USER, content=prompt))
    response = _parse_response(_openai_exchange(context))
    return response


def _parse_response(gpt_response: str) -> dict:
    return json.loads(gpt_response)
