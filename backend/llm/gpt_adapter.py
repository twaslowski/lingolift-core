import logging
import os

import json5 as json
from openai import OpenAI

from llm.message import Message

api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)


def openai_exchange(messages: list[Message], json_mode: bool = False) -> dict:
    """
    Abstraction layer for the OpenAI API.
    :param messages: List of message objects to emulate session state.
    Usually just contains System prompt and User request.
    :param json_mode: Whether to use LLM JSON mode. Defaults to False as OpenAI forcibly generates JSONs with an
    object root, not lists, even when instructed otherwise.
    :return: JSON response of LLM
    Note: If this was used in an interactive chat context, this should return a Message() object to track session state.
    However, in this context, we're simply consuming the responses without need for state, so this is fine.
    """
    logging.info(f"message: {messages[1].content}")
    response_format = "json_object" if json_mode else "text"
    # mypy complains about the usage of the create() function, but clearly it works
    completion = client.chat.completions.create(  # type: ignore
        model="gpt-3.5-turbo-1106",
        response_format={"type": response_format},
        messages=[message.asdict() for message in messages]
    )
    response = completion.choices[0].message.content
    logging.info(f"Received response: {response}")
    return parse_response(response)


def parse_response(gpt_response: str) -> dict:
    # Sometimes, llm will hallucinate '```json' at the start of the JSON it returns. This solves that.
    cleaned_response = gpt_response.replace('`', '').replace('json', '')
    return json.loads(cleaned_response)
