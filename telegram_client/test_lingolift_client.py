import asyncio
import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

from shared.client import Client
from shared.exception import ApplicationException
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

import app


class TestLingoliftClient(IsolatedAsyncioTestCase):

    async def test_concurrency_works(self):
        start = datetime.datetime.now()
        print(f"started at {start}")

        client = Client()
        client.get_suggestions = AsyncMock(side_effect=delayed_response)
        client.get_literal_translation = AsyncMock(side_effect=delayed_response)
        client.get_syntactical_analysis = AsyncMock(side_effect=delayed_response)

        await asyncio.gather(
            client.fetch_response_suggestions("test"),
            client.fetch_translation("test"),
            client.fetch_syntactical_analysis("test", "test"),
        )

        end = datetime.datetime.now()
        print(f"finished at {end}")
        self.assertLessEqual((end - start).total_seconds(), 3)

    async def test_translation_errors(self):
        client = Client()
        # if translation fails
        client.fetch_translation = AsyncMock(side_effect=ApplicationException("some-error"))

        # set up mocks
        app.reply = AsyncMock()
        app.stringifier = Mock()
        update = Mock()
        update.message.text = "test"

        # when message is processed
        await app.handle_text_message(update, None)

        # then only the introductory and the error message should be sent
        self.assertEqual(2, app.reply.call_count)
        self.assertEqual(0, app.stringifier.call_count)
        self.assertEqual(app.MESSAGE_RECEIVED, app.reply.call_args_list[0][0][1])
        # ensure there is overlap between Translation Error message and received error message
        # the formatting makes it difficult to perform exact matching, but this is close enough
        self.assertIn(app.TRANSLATION_ERROR[:20], app.reply.call_args_list[1][0][1])

    @staticmethod
    def mock_get_suggestions() -> list[ResponseSuggestion]:
        return [ResponseSuggestion(suggestion="test", translation="test")]

    @staticmethod
    def mock_get_translation() -> Translation:
        return Translation(translation="test", language_code="XY", language_name="test")


async def delayed_response():
    await asyncio.sleep(2)
    return "mock response"
