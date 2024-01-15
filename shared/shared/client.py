import requests

from shared.model.error import ApplicationError
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation

TRANSLATIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching translations from backend"
LITERAL_TRANSLATIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching translations from backend"
SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching syntactical analysis from backend"
RESPONSE_SUGGESTIONS_UNEXPECTED_ERROR = "An unexpected error occurred when fetching response suggestions from backend"


class Client:
    """
    Defines common methods to interact with the lingolift backend API.
    Includes error handling and parsing to the pydantic models.
    """

    def __init__(self, endpoint: str = "localhost", port: str = "5001"):
        self.endpoint = endpoint
        self.port = port
        self.url = f"https://{self.endpoint}:{self.port}"

    async def fetch_translation(self, sentence: str) -> Translation | ApplicationError:
        """
        Interacts with the /translation endpoint of the backend API.
        :param sentence: Sentence to translate
        :return: Translation object in case of a 200 status code, ApplicationError otherwise
        """
        print(f"fetching translation for sentence '{sentence}'")
        response = requests.post(f"{self.url}/translation", json={"sentence": sentence})
        print(f"received translation for sentence '{sentence}': '{response}'")
        match response.status_code:
            case 200:
                return Translation(**response.json())
            # no expected error on the backend side, so no need to handle 400
            case _:
                return ApplicationError(error_message=TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_literal_translations(self, sentence: str) -> list[LiteralTranslation] | ApplicationError:
        """
        Interacts with the /literal-translation endpoint of the backend API.
        :param sentence: Sentence for which to fetch literal translations
        :return: list of LiteralTranslation objects in case of a 200 status code, ApplicationError otherwise
        """
        response = requests.post(f"{self.url}/literal-translation", json={"sentence": sentence})
        match response.status_code:
            case 200:
                response = response.json()
                print(f"Received literal translations for sentence '{sentence}': '{response}'")
                return [LiteralTranslation(**literal_translation) for literal_translation in response]
            case 400:
                return ApplicationError(**response.json())
            case _:
                return ApplicationError(error_message=LITERAL_TRANSLATIONS_UNEXPECTED_ERROR)

    async def fetch_syntactical_analysis(self, sentence: str, language: str) -> \
            list[SyntacticalAnalysis] | ApplicationError:
        """
        Interacts with the /syntactical-analysis endpoint of the backend API.
        :param sentence: Sentence for which to fetch syntactical analysis
        :param language: Source language of the sentence; required for choosing correct spaCy model
        :return: list of SyntacticalAnalysis objects in case of a 200 status code, ApplicationError otherwise
        """
        response = requests.post(f"{self.url}/syntactical-analysis", json={"sentence": sentence, "language": language})
        match response.status_code:
            case 200:
                analyses = response.json()
                print(f"Received syntactical analysis for sentence '{sentence}': '{analyses}'")
                return [SyntacticalAnalysis(**analysis) for analysis in analyses]
            case 400:
                return ApplicationError(**response.json())
            case _:
                return ApplicationError(error_message=SYNTACTICAL_ANALYSIS_UNEXPECTED_ERROR)

    async def fetch_response_suggestions(self, sentence: str) -> list[ResponseSuggestion] | ApplicationError:
        """
        Interacts with the /response-suggestion endpoint of the backend API.
        :param sentence: Sentence for which to fetch response suggestions
        :return: list of ResponseSuggestion objects in case of a 200 status code, ApplicationError otherwise
        """
        response = requests.post(f"{self.url}/response-suggestion", json={"sentence": sentence})
        match response.status_code:
            case 200:
                suggestions = response.json()
                print(f"Received response suggestions for sentence '{sentence}': '{suggestions}'")
                return [ResponseSuggestion(**suggestion) for suggestion in suggestions]
            case 400:
                return ApplicationError(**response.json())
            case _:
                return ApplicationError(error_message=RESPONSE_SUGGESTIONS_UNEXPECTED_ERROR)
