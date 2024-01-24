import logging

import aiohttp
import requests  # type: ignore[import-untyped]

from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation
from shared.model.upos_explanation import UposExplanation

TRANSLATIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching translations from backend"
LITERAL_TRANSLATIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching translations from backend"
SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching syntactical analysis from backend"
RESPONSE_SUGGESTIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching response suggestions from backend"
UPOS_EXPLANATIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching UPOS explanations from backend"


class Client:
    """
    Defines common methods to interact with the backend API.
    Includes error handling and parsing to the pydantic models.
    """

    def __init__(self, protocol: str = "https", host: str = "localhost", port: str = "5001"):
        self.protocol = protocol
        self.endpoint = host
        self.port = port
        self.url = f"{self.protocol}://{self.endpoint}:{self.port}"

    async def fetch_translation(self, sentence: str) -> Translation:
        """
        Interacts with the /translation endpoint of the backend API.
        :param sentence: Sentence to translate
        :return: Translation object in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching translation for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/translation", json={"sentence": sentence}) as response:
                data = await response.json()
                logging.info(f"received /translation response for sentence '{sentence}': '{data}'")

                if response.status == 200:
                    return Translation(**data)
                elif response.status == 400:
                    logging.error(f"Received /translation error for sentence '{sentence}': '{data}'")
                    raise ApplicationException(**data)
                else:
                    raise ApplicationException(error_message=TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_literal_translations(self, sentence: str) -> list[LiteralTranslation]:
        """
        Interacts with the /literal-translation endpoint of the backend API.
        :param sentence: Sentence for which to fetch literal translations
        :return: list of LiteralTranslation objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching literal translations for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/literal-translation", json={"sentence": sentence}) as response:
                if response.status == 200:
                    literal_translations = await response.json()
                    logging.info(
                        f"Received /literal-translation response for sentence '{sentence}': '{literal_translations}'")
                    return [LiteralTranslation(**literal_translation) for literal_translation in literal_translations]
                elif response.status == 400:
                    error_data = await response.json()
                    logging.error(f"Received /literal-translation error for sentence '{sentence}': '{error_data}'")
                    raise ApplicationException(**error_data)
                else:
                    raise ApplicationException(error_message=LITERAL_TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_syntactical_analysis(self, sentence: str) -> list[SyntacticalAnalysis]:
        """
        Interacts with the /syntactical-analysis endpoint of the backend API.
        :param sentence: Sentence for which to fetch syntactical analysis
        :return: list of SyntacticalAnalysis objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching syntactical analysis for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/syntactical-analysis", json={"sentence": sentence}) as response:
                if response.status == 200:
                    analyses = await response.json()
                    logging.info(f"Received syntactical analysis for sentence '{sentence}': '{analyses}'")
                    return [SyntacticalAnalysis(**analysis) for analysis in analyses]
                elif response.status == 400:
                    error_data = await response.json()
                    logging.error(f"Received /syntactical-analysis error for sentence '{sentence}': '{error_data}'")
                    raise ApplicationException(**error_data)
                else:
                    raise ApplicationException(error_message=SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR)

    async def fetch_response_suggestions(self, sentence: str) -> list[ResponseSuggestion]:
        """
        Interacts with the /response-suggestion endpoint of the backend API.
        :param sentence: Sentence for which to fetch response suggestions
        :return: list of ResponseSuggestion objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching response suggestions for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.url}/response-suggestion", json={"sentence": sentence}) as response:
                if response.status == 200:
                    suggestions = await response.json()
                    logging.info(f"Received response suggestions for sentence '{sentence}': '{suggestions}'")
                    return [ResponseSuggestion(**suggestion) for suggestion in suggestions]
                elif response.status == 400:
                    error_data = await response.json()
                    logging.error(f"Received /response-suggestion error for sentence '{sentence}': '{error_data}'")
                    raise ApplicationException(**error_data)
                else:
                    raise ApplicationException(error_message=RESPONSE_SUGGESTIONS_UNEXPECTED_ERROR)

    async def fetch_upos_explanation(self, syntactical_analysis: SyntacticalAnalysis) -> UposExplanation:
        """
        Interacts with the /syntactical-analysis/upos-explanation endpoint of the backend API.
        :param syntactical_analysis: SyntacticalAnalysis object for which to fetch upos explanations
        :return: list of UposExplanation objects in case of a 200 status code, ApplicationException otherwise
        """
        payload = {"upos": syntactical_analysis.pos, "word": syntactical_analysis.word}
        response = requests.post(f"{self.url}/syntactical-analysis/upos-explanation",
                                 json=payload)
        if response.status_code == 200:
            explanations = response.json()
            logging.info(
                f"Received upos explanations for syntactical analysis '{syntactical_analysis}': '{explanations}'")
            return UposExplanation(**explanations)
        else:
            raise ApplicationException(error_message=UPOS_EXPLANATIONS_UNEXPECTED_ERROR)

    async def fetch_health(self) -> requests.Response:
        """
        Interacts with the /health endpoint of the backend API.
        :return: requests.Response object
        """
        return requests.get(f"{self.url}/health")
