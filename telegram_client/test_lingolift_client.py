import asyncio
import datetime
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from telegram_client import lingolift_client


class TestLingoliftClient(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        async def delayed_response():
            await asyncio.sleep(2)
            return "mock response"

        lingolift_client.get_suggestions = AsyncMock(side_effect=delayed_response)
        lingolift_client.get_literal_translation = AsyncMock(side_effect=delayed_response)
        lingolift_client.get_syntactical_analysis = AsyncMock(side_effect=delayed_response)

    async def test_true(self):
        start = datetime.datetime.now()
        print(f"started at {start}")

        async with asyncio.TaskGroup() as tg:
            suggestions = tg.create_task(lingolift_client.get_suggestions())
            lt = tg.create_task(lingolift_client.get_literal_translation())
            sa = tg.create_task(lingolift_client.get_syntactical_analysis())
            # Wait for all tasks to complete
            await suggestions
            await lt
            await sa

        end = datetime.datetime.now()
        print(f"finished at {end}")
        self.assertLessEqual((end - start).total_seconds(), 3)
