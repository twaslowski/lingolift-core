import logging
import json

from shared.exception import ApplicationException

from nlp.language_detection import LanguageNotAvailableException
from nlp.syntactical_analysis import perform_analysis

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def syntactical_analysis_handler(event, _):
    body = json.loads(event.get('body'))
    sentence = body.get('sentence')
    logging.info(f"Received sentence, language: {sentence}")
    try:
        analyses = perform_analysis(sentence)
        return ok([a.model_dump() for a in analyses])
    except LanguageNotAvailableException as e:
        return fail(ApplicationException(e.error_message), 400)


def ok(res: dict | list) -> dict:
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(res)
    }


def fail(e: ApplicationException, status: int) -> dict:
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(e.dict())
    }
