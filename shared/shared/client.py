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

    async def fetch_literal_translations(self, sentence: str) -> list[LiteralTranslation] | ApplicationError:
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
        response = requests.post(f"{self.url}/syntactical-analysis", json={"sentence": sentence, "language": language})
        if response.status_code != 200:
            return ApplicationError(**response.json())
        else:
            analyses = response.json()
            print(f"Received syntactical analysis for sentence '{sentence}': '{analyses}'")
            return [SyntacticalAnalysis(**analysis) for analysis in analyses]

    async def fetch_response_suggestions(self, sentence: str) -> list[ResponseSuggestion] | ApplicationError:
        response = requests.post(f"{self.url}/response-suggestion", json={"sentence": sentence})
        if response.status_code != 200:
            return ApplicationError(**response.json())
        else:
            suggestions = response.json()
            print(f"Received response suggestions for sentence '{sentence}': '{suggestions}'")
            return [ResponseSuggestion(**suggestion) for suggestion in suggestions]

    def fetch_translation(self, sentence: str) -> Translation | ApplicationError:
        print(f"fetching translation for sentence '{sentence}'")
        response = requests.post(f"{self.url}/translation", json={"sentence": sentence})
        print(f"received translation for sentence '{sentence}': '{response}'")
        if response.status_code != 200:
            return ApplicationError(error_message=TRANSLATIONS_UNEXPECTED_ERROR)
        else:
            return Translation(**response.json())
