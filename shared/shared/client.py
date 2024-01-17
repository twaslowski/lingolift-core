from typing import Union

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

    async def fetch_translation(self, sentence: str) -> Union[Translation, ApplicationException]:
        """
        Interacts with the /translation endpoint of the backend API.
        :param sentence: Sentence to translate
        :return: Translation object in case of a 200 status code, ApplicationException otherwise
        """
        print(f"fetching translation for sentence '{sentence}'")
        response = requests.post(f"{self.url}/translation", json={"sentence": sentence})
        print(f"received translation for sentence '{sentence}': '{response}'")
        if response.status_code == 200:
            return Translation(**response.json())
        # no expected error on the backend side, so no need to handle 400
        else:
            return ApplicationException(error_message=TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_literal_translations(self, sentence: str) -> Union[list[LiteralTranslation], ApplicationException]:
        """
        Interacts with the /literal-translation endpoint of the backend API.
        :param sentence: Sentence for which to fetch literal translations
        :return: list of LiteralTranslation objects in case of a 200 status code, ApplicationException otherwise
        """
        response = requests.post(f"{self.url}/literal-translation", json={"sentence": sentence})
        if response.status_code == 200:
            response = response.json()
            print(f"Received literal translations for sentence '{sentence}': '{response}'")
            return [LiteralTranslation(**literal_translation) for literal_translation in response]
        elif response.status_code == 400:
            return ApplicationException(**response.json())
        else:
            return ApplicationException(error_message=LITERAL_TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_syntactical_analysis(self, sentence: str, language: str) -> \
            Union[list[SyntacticalAnalysis], ApplicationException]:
        """
        Interacts with the /syntactical-analysis endpoint of the backend API.
        :param sentence: Sentence for which to fetch syntactical analysis
        :param language: Source language of the sentence; required for choosing correct spaCy model
        :return: list of SyntacticalAnalysis objects in case of a 200 status code, ApplicationException otherwise
        """
        response = requests.post(f"{self.url}/syntactical-analysis", json={"sentence": sentence, "language": language})
        if response.status_code == 200:
            analyses = response.json()
            print(f"Received syntactical analysis for sentence '{sentence}': '{analyses}'")
            return [SyntacticalAnalysis(**analysis) for analysis in analyses]
        elif response.status_code == 400:
            return ApplicationException(**response.json())
        else:
            return ApplicationException(error_message=SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR)

    async def fetch_response_suggestions(self, sentence: str) -> Union[list[ResponseSuggestion], ApplicationException]:
        """
        Interacts with the /response-suggestion endpoint of the backend API.
        :param sentence: Sentence for which to fetch response suggestions
        :return: list of ResponseSuggestion objects in case of a 200 status code, ApplicationException otherwise
        """
        response = requests.post(f"{self.url}/response-suggestion", json={"sentence": sentence})
        if response.status_code == 200:
            suggestions = response.json()
            print(f"Received response suggestions for sentence '{sentence}': '{suggestions}'")
            return [ResponseSuggestion(**suggestion) for suggestion in suggestions]
        elif response.status_code == 400:
            return ApplicationException(**response.json())
        else:
            return ApplicationException(error_message=RESPONSE_SUGGESTIONS_UNEXPECTED_ERROR)

    async def fetch_upos_explanation(self, syntactical_analysis: SyntacticalAnalysis) -> \
            Union[UposExplanation, ApplicationException]:
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
            print(f"Received upos explanations for syntactical analysis '{syntactical_analysis}': '{explanations}'")
            return UposExplanation(**explanations)
        else:
            return ApplicationException(error_message=UPOS_EXPLANATIONS_UNEXPECTED_ERROR)
