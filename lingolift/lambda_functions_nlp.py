import json
import logging

from lingolift.nlp.morphologizer import retrieve_all_inflections
from lingolift.nlp.syntactical_analysis import perform_analysis
from shared.exception import ApplicationException, LanguageNotAvailableException
from lingolift.util.lambda_proxy_return import check_pre_warm, fail, ok

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)


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
    inflections = retrieve_all_inflections(word)
    return ok(inflections.model_dump())
