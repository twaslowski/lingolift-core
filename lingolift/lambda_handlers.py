import json
import logging

import iso639
from shared.exception import (
    ApplicationException,
    LanguageNotAvailableException,
    LanguageNotIdentifiedException,
    SentenceTooLongException,
)

from lingolift.lambda_context_container import ContextContainer
from lingolift.nlp.syntactical_analysis import perform_analysis
from lingolift.util.lambda_proxy import check_pre_warm, fail, ok

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

# instantiate context object
context_container = ContextContainer()


def translation_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    try:
        response = context_container.translation_generator.generate_translation(
            sentence
        )
        return ok(response.model_dump())
    except iso639.LanguageNotFoundError:
        logger.error(f"Language for sentence {sentence} could not be identified.")
        return fail(LanguageNotIdentifiedException(), 400)


def response_suggestion_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    response = (
        context_container.response_suggestion_generator.generate_response_suggestions(
            sentence
        )
    )
    return ok([r.model_dump() for r in response])


def literal_translation_handler(event, _):
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence: {sentence}")
    try:
        response = context_container.literal_translation_generator.generate_literal_translation(
            sentence
        )
        return ok([r.model_dump() for r in response])
    except SentenceTooLongException as e:
        logger.error(f"Sentence {sentence} too long for literal translation.")
        return fail(e, 400)


def syntactical_analysis_handler(event, _) -> dict:
    if pre_warm_response := check_pre_warm(event):
        return pre_warm_response
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    logger.info(f"Received sentence, language: {sentence}")
    try:
        analyses = perform_analysis(sentence)
        return ok([a.model_dump() for a in analyses])
    except LanguageNotAvailableException as e:
        return fail(ApplicationException(e.error_message), 400)


def inflection_handler(event, _) -> dict:
    if pre_warm_response := check_pre_warm(event):
        return pre_warm_response
    body = json.loads(event.get("body"))
    word = body.get("word")
    inflections = context_container.morphologizer.retrieve_all_inflections(word)
    return ok(inflections.model_dump())
