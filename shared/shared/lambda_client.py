import asyncio
import json
import logging
from typing import Tuple

import boto3

from shared.exception import ApplicationException
from shared.model.syntactical_analysis import SyntacticalAnalysis
from shared.model.translation import Translation
from shared.model.literal_translation import LiteralTranslation
from shared.model.response_suggestion import ResponseSuggestion


class LambdaClient:
    def __init__(self, access_key_id: str, secret_access_key: str, region: str):
        self.lambda_client = boto3.client(
            'lambda',
            region_name=region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )

    async def fetch_translation(self, sentence: str) -> Translation:
        response = self.lambda_client.invoke(
            FunctionName="translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        status_code, body = retrieve_payload(response)
        if status_code == 200:
            return Translation(**body)
        else:
            raise ApplicationException(**body)

    async def fetch_literal_translations(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="literal_translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        status_code, body = retrieve_payload(response)
        if status_code == 200:
            return [LiteralTranslation(**literal_translation) for literal_translation in body]
        else:
            raise ApplicationException(**body)

    async def fetch_response_suggestions(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="response_suggestion-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        status_code, body = retrieve_payload(response)
        if status_code == 200:
            return [ResponseSuggestion(**suggestion) for suggestion in body]
        else:
            raise ApplicationException(**body)

    async def fetch_syntactical_analysis(self, sentence: str, language: str):
        response = self.lambda_client.invoke(
            FunctionName="syntactical_analysis-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence, "language": language})
        )
        try:
            status_code, body = retrieve_payload(response)
            if status_code == 200:
                return [SyntacticalAnalysis(**a) for a in body]
            else:
                raise ApplicationException(**body)
        except Exception:
            raise ApplicationException("Unknown error occurred.")


def retrieve_payload(lambda_response: dict) -> Tuple[int, dict]:
    try:
        payload = json.loads(lambda_response.get('Payload').read().decode())
        logging.info(f"Received lambda response: {payload}")
        status_code = payload.get('status_code')
        body = payload.get('body')
        if isinstance(body, str):
            body = json.loads(body)
        return status_code, body
    except json.JSONDecodeError:
        raise ApplicationException("Could not parse response from backend.")


if __name__ == '__main__':
    import os

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    client = LambdaClient(os.getenv("ACCESS_KEY_ID"),
                          os.getenv("SECRET_ACCESS_KEY"),
                          "eu-central-1")
    logging.info(asyncio.run(client.fetch_literal_translations("Wie viel kostet das Bier?")))
