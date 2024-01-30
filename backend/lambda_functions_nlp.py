import logging
import json

from shared.exception import ApplicationException

from nlp.language_detection import LanguageNotAvailableException
from nlp.syntactical_analysis import perform_analysis
from util.lambda_proxy_return import ok, fail

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)


def syntactical_analysis_handler(event, _):
    body = json.loads(event.get('body'))
    sentence = body.get('sentence')
    logger.info(f"Received sentence, language: {sentence}")
    try:
        analyses = perform_analysis(sentence)
        return ok([a.model_dump() for a in analyses])
    except LanguageNotAvailableException as e:
        return fail(ApplicationException(e.error_message), 400)
