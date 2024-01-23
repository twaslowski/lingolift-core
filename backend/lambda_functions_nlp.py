import logging

from iso639 import LanguageNotFoundError
from shared.exception import ApplicationException

from nlp.syntactical_analysis import perform_analysis, LanguageNotAvailableException


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def syntactical_analysis_handler(event, _):
    sentence = event.get('sentence')
    language = event.get('language')
    logging.info(f"Received sentence, language: {sentence}, {language}")
    try:
        analyses = perform_analysis(sentence, language)
        return {
            "status_code": 200,
            "body": [a.model_dump() for a in analyses]
        }
    except LanguageNotFoundError | LanguageNotAvailableException as e:
        return {
            "status_code": 400,
            "body": ApplicationException(e.error_message).dict()
        }
    except Exception as e:
        logging.error(e)
        return {
            "status_code": 500,
            "body": ApplicationException(f"Unknown error occurred: {e}").dict()
        }
