import requests

from shared.model.error import ApplicationError
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation

"""
Defines common methods to interact with the lingolift backend API. 
Includes error handling and parsing to the pydantic models.
"""


async def fetch_literal_translations(sentence: str) -> list[LiteralTranslation] | ApplicationError:
    response = requests.post("http://localhost:5001/literal-translation", json={"sentence": sentence})
    if response.status_code != 200:
        return ApplicationError(**response.json())
    else:
        response = response.json()
        print(f"Received literal translations for sentence '{sentence}': '{response}'")
        return [LiteralTranslation(**literal_translation) for literal_translation in response]


async def fetch_syntactical_analysis(sentence: str, language: str) -> list[SyntacticalAnalysis] | ApplicationError:
    response = requests.post("http://localhost:5001/syntactical-analysis",
                             json={"sentence": sentence, "language": language})
    if response.status_code != 200:
        return ApplicationError(**response.json())
    else:
        analyses = response.json()
        print(f"Received syntactical analysis for sentence '{sentence}': '{analyses}'")
        return [SyntacticalAnalysis(**analysis) for analysis in analyses]


async def fetch_response_suggestions(sentence: str) -> list[ResponseSuggestion] | ApplicationError:
    response = requests.post("http://localhost:5001/response-suggestion", json={"sentence": sentence})
    if response.status_code != 200:
        return ApplicationError(**response.json())
    else:
        suggestions = response.json()
        print(f"Received response suggestions for sentence '{sentence}': '{suggestions}'")
        return [ResponseSuggestion(**suggestion) for suggestion in suggestions]


def fetch_translation(sentence: str) -> Translation | ApplicationError:
    print(f"fetching translation for sentence '{sentence}'")
    response = requests.post("http://localhost:5001/translation", json={"sentence": sentence})
    print(f"received translation for sentence '{sentence}': '{response}'")
    if response.status_code != 200:
        return ApplicationError(**response.json())
    else:
        return Translation(**response.json())
