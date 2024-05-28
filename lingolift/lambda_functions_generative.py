import json
import logging
import os

import iso639
from shared.exception import *

from lingolift.generative.literal_translation import generate_literal_translation
from lingolift.generative.response_suggestion import generate_response_suggestions
from lingolift.generative.translation import generate_translation
from lingolift.llm.gpt_adapter import GPTAdapter
from lingolift.util.lambda_proxy_return import fail, ok

"""
This module contains the handlers for the AWS Lambda functions that are responsible for the generative tasks of the
lingolift application, i.e. translation and language identification of sentences, literal translation of words
and the generation of response suggestions.

Since Lambda requires functions to be top-level, the handlers are defined as top-level functions.
Therefore, some boilerplate code that I would like to encapsulate as a class needs to exist at top-level as well.
"""

# configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)

# configure GPT adapter
openai_api_key = os.getenv("OPENAI_API_KEY")
gpt_adapter = GPTAdapter(openai_api_key)


def translation_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    try:
        response = generate_translation(sentence, gpt_adapter)
        return ok(response.model_dump())
    except iso639.LanguageNotFoundError:
        logger.error(f"Language for sentence {sentence} could not be identified.")
        return fail(LanguageNotIdentifiedException(), 400)


def response_suggestion_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    response = generate_response_suggestions(sentence)
    return ok([r.model_dump() for r in response])


def literal_translation_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    try:
        response = generate_literal_translation(sentence)
        return ok([r.model_dump() for r in response])
    except SentenceTooLongException as e:
        logger.error(f"Sentence {sentence} too long for literal translation.")
        return fail(e, 400)
