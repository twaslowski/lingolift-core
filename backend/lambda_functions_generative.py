import iso639
from shared.exception import ApplicationException

from generative.response_suggestion import generate_response_suggestions
from generative.translation import generate_translation
from generative.literal_translation import generate_literal_translation
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def translation_handler(event, _):
    sentence = event.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_translation(sentence)
        return {
            "status_code": 200,
            "body": response.model_dump()
        }
    except iso639.LanguageNotFoundError:
        return {
            "status_code": 400,
            "body": ApplicationException(f"Language for sentence {sentence} could not be identified.").dict()
        }
    except Exception as e:
        logging.error(e)
        return {
            "status_code": 500,
            "body": ApplicationException(f"Unknown error occurred: {e}").dict()
        }


def response_suggestion_handler(event, _):
    sentence = event.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_response_suggestions(sentence)
        return {
            "status_code": 200,
            "body": [r.model_dump() for r in response]
        }
    except Exception as e:
        logging.error(e)
        return {
            "status_code": 500,
            "body": ApplicationException(f"Unknown error occurred: {e}").dict()
        }


def literal_translation_handler(event, _):
    sentence = event.get('sentence')
    logging.info(f"Received sentence: {sentence}")
    try:
        response = generate_literal_translation(sentence)
        return {
            "status_code": 200,
            "body": [r.model_dump() for r in response]
        }
    except Exception as e:
        logging.error(e)
        return {
            "status_code": 500,
            "body": ApplicationException(f"Unknown error occurred: {e}").dict()
        }
