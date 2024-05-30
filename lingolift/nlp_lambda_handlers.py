import json
import logging

from nlp.syntactical_analysis import perform_analysis
from nlp_lambda_context_container import NLPLambdaContextContainer
from shared.exception import (
    LanguageNotAvailableException,
    LanguageNotIdentifiedException,
)
from util.lambda_proxy import check_pre_warm, fail, ok

"""
The split into lambda_handlers and lambda_handlers_nlp is unfortunately required.
When importing from the syntactical_analysis module, spaCy gets imported transitively.
For memory reasons, spaCy is only included where required.
"""

# configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)

# instantiate context object
context_container = NLPLambdaContextContainer()


def syntactical_analysis_handler(event, _) -> dict:
    if pre_warm_response := check_pre_warm(event):
        return pre_warm_response
    body = json.loads(event.get("body"))
    sentence = body.get("sentence")
    language_code = body.get("language_code")
    logger.info(
        f"Received sentence, language: {sentence}, language_code: {language_code}"
    )
    try:
        analyses = perform_analysis(sentence, language_code)
        return ok([a.model_dump() for a in analyses])
    except (LanguageNotAvailableException, LanguageNotIdentifiedException) as e:
        return fail(e, 400)


def inflection_handler(event, _) -> dict:
    if pre_warm_response := check_pre_warm(event):
        return pre_warm_response
    body = json.loads(event.get("body"))
    word = body.get("word")
    inflections = context_container.morphologizer.retrieve_all_inflections(word)
    return ok(inflections.model_dump())
