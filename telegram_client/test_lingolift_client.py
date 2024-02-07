from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

from shared.client import Client
from shared.exception import ApplicationException
from shared.model.response_suggestion import ResponseSuggestion
from shared.model.translation import Translation

import app


class TestLingoliftClient(IsolatedAsyncioTestCase):
    async def test_translation_errors(self):
        app.client = Client("")
        # if translation fails
        app.client.fetch_translation = AsyncMock(side_effect=self.mock_error())

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
        self.assertIn("some-error", app.reply.call_args_list[1][0][1])

    async def test_syntactical_analysis_errors(self):
        app.client = Mock()
        # if syntactical analysis fails
        app.client.fetch_translation = AsyncMock(
            return_value=self.mock_get_translation()
        )
        app.client.fetch_literal_translations = AsyncMock(side_effect=self.mock_error())

        # set up mocks
        app.reply = AsyncMock()
        app.stringifier = Mock()
        update = Mock()
        update.message.text = "test"

        # when message is processed
        await app.handle_text_message(update, None)

        # assert latest reply() count contains ANALYSIS_ERROR
        self.assertIn("some-error", app.reply.call_args_list[-1][0][1])

    @staticmethod
    def mock_get_suggestions() -> list[ResponseSuggestion]:
        return [ResponseSuggestion(suggestion="test", translation="test")]

    @staticmethod
    def mock_get_translation() -> Translation:
        return Translation(translation="test", language_code="XY", language_name="test")

    @staticmethod
    def mock_error() -> ApplicationException:
        return ApplicationException(error_message="some-error")
