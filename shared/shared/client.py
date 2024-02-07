import logging

import aiohttp
from aiohttp.client_reqrep import ClientResponse

from shared.exception import ApplicationException
from shared.model.inflection import Inflection, Inflections
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation


class Client:
    """
    Defines common methods to interact with the backend API.
    Includes error handling and parsing to the pydantic models.
    """

    def __init__(self, host):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.host = host

    async def fetch_translation(self, sentence: str) -> Translation:
        """
        Interacts with the /translation endpoint of the backend API.
        :param sentence: Sentence to translate
        :return: Translation object in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching translation for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/translation", json={"sentence": sentence}
            ) as response:
                data = await response.json()
                logging.info(
                    f"received /translation response for sentence '{sentence}': '{data}'"
                )

                if response.status == 200:
                    return Translation(**data)
                else:
                    await self.handle_failure("translation", response)

    async def fetch_literal_translations(
        self, sentence: str
    ) -> list[LiteralTranslation]:
        """
        Interacts with the /literal-translation endpoint of the backend API.
        :param sentence: Sentence for which to fetch literal translations
        :return: list of LiteralTranslation objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching literal translations for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/literal-translation", json={"sentence": sentence}
            ) as response:
                if response.status == 200:
                    literal_translations = await response.json()
                    logging.info(
                        f"Received /literal-translation response for sentence '{sentence}': '{literal_translations}'"
                    )
                    return [
                        LiteralTranslation(**literal_translation)
                        for literal_translation in literal_translations
                    ]
                else:
                    await self.handle_failure("literal-translation", response)

    async def fetch_syntactical_analysis(
        self, sentence: str
    ) -> list[SyntacticalAnalysis]:
        """
        Interacts with the /syntactical-analysis endpoint of the backend API.
        :param sentence: Sentence for which to fetch syntactical analysis
        :return: list of SyntacticalAnalysis objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching syntactical analysis for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/syntactical-analysis", json={"sentence": sentence}
            ) as response:
                if response.status == 200:
                    analyses = await response.json()
                    logging.info(
                        f"Received syntactical analysis for sentence '{sentence}': '{analyses}'"
                    )
                    return [SyntacticalAnalysis(**analysis) for analysis in analyses]
                else:
                    await self.handle_failure("syntactical-analysis", response)

    async def fetch_response_suggestions(
        self, sentence: str
    ) -> list[ResponseSuggestion]:
        """
        Interacts with the /response-suggestion endpoint of the backend API.
        :param sentence: Sentence for which to fetch response suggestions
        :return: list of ResponseSuggestion objects in case of a 200 status code, ApplicationException otherwise
        """
        logging.info(f"fetching response suggestions for sentence '{sentence}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/response-suggestion", json={"sentence": sentence}
            ) as response:
                if response.status == 200:
                    suggestions = await response.json()
                    logging.info(
                        f"Received response suggestions for sentence '{sentence}': '{suggestions}'"
                    )
                    return [
                        ResponseSuggestion(**suggestion) for suggestion in suggestions
                    ]
                else:
                    await self.handle_failure("response-suggestion", response)

    async def fetch_inflections(self, word: str) -> Inflections:
        logging.info(f"fetching inflections for word '{word}'")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.host}/inflection", json={"word": word}
            ) as response:
                if response.status == 200:
                    inflections = await response.json()
                    logging.info(
                        f"Received inflections for word '{word}': '{inflections}'"
                    )
                    return Inflections(**inflections)
                else:
                    await self.handle_failure("inflection", response)

    @staticmethod
    async def handle_failure(endpoint: str, response: ClientResponse):
        error_data = await response.json()
        if response.status == 400:
            logging.error(
                f"Received 400 status code on {endpoint}. Error: '{error_data}'"
            )
            raise ApplicationException(**error_data)
        else:
            logging.error(
                f"Received unexpected error from {endpoint}: {response.status}, {error_data}"
            )
            raise ApplicationException(error_message=error_data)
