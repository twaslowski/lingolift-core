import json
import logging

from shared.exception import ApplicationException, LanguageNotAvailableException

from lingolift.nlp.morphologizer import Morphologizer
from lingolift.nlp.syntactical_analysis import perform_analysis

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
