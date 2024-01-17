import asyncio
import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from shared.client import Client


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


async def delayed_response():
    await asyncio.sleep(2)
    return "mock response"
