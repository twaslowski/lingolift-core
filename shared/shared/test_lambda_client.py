from shared.lambda_client import LambdaClient
from unittest import IsolatedAsyncioTestCase


class TestLambdaClient(IsolatedAsyncioTestCase):
    """
    Tests the shared client methods that are used by both the frontend and the telegram bot.
    This only tests for happy paths (200 status codes),
    expected errors (400 status codes with the backend error object),
    and unexpected errors (500 status codes). There is no need to test for JSON structure as the backend only
    sends responses that adhere to the shared pydantic models defined in the `shared.model` package.
    """

    async def test_translation_happy_path(self):
        client = LambdaClient(access_key_id, secret_access_key, region)
        print(client.fetch_translation("adklnasd?"))
