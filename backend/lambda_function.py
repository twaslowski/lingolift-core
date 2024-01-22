import json

import iso639
from shared.exception import ApplicationException

from service.generate import generate_translation, generate_literal_translations, generate_responses
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def translation_handler(event, _):
    sentence = event.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_translation(sentence)
        return {
            "status_code": 200,
            "body": json.dumps(response.model_dump())
        }
    except iso639.LanguageNotFoundError:
        return {
            "status_code": 400,
            "body": json.dumps(
                ApplicationException(f"Language for sentence {sentence} could not be identified.").dict())
        }


def response_suggestion_handler(event, _):
    return [r.model_dump() for r in generate_responses(event.get('sentence'))]


def literal_translation_handler(event, _):
    return [r.model_dump() for r in generate_literal_translations(event.get('sentence'))]
