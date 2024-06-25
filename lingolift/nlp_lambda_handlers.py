import json
import logging

from lingolift.nlp.syntactical_analysis import perform_analysis
from lingolift.nlp_lambda_context_container import NLPLambdaContextContainer
from lingolift.util.lambda_proxy import check_pre_warm, ok

"""
The split into the lambda_handlers and lambda_handlers_nlp files is unfortunately required.
When importing from the syntactical_analysis module, spaCy gets imported transitively.
For memory reasons, spaCy is only included where required, so its import will fail in the non-dockerized lambdas.
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
    logger.info(f"Received sentence, language: {sentence}")
    analyses = perform_analysis(sentence)
    return ok([a.dict() for a in analyses])


def inflection_handler(event, _) -> dict:
    if pre_warm_response := check_pre_warm(event):
        return pre_warm_response
    body = json.loads(event.get("body"))
    word = body.get("word")
    inflections = context_container.morphologizer.retrieve_all_inflections(word)
    return ok(inflections.model_dump())
