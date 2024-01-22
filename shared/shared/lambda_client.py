import asyncio
import json
import logging

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
        response_body = response.get('Payload').read()
        logging.info(f"Received lambda response: {response_body}")
        try:
            payload = json.loads(response_body)
            status_code = payload.get('status_code')
            if status_code == 200:
                body = json.loads(payload.get('body'))
                return Translation(**body)
            else:
                error = json.loads(payload.get('body'))
                raise ApplicationException(**error)
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    async def fetch_literal_translations(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="literal_translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        response_body = response.get('Payload').read()
        logging.info(f"Received lambda response: {response_body}")
        try:
            payload = json.loads(response_body)
            status_code = payload.get('status_code')
            if status_code == 200:
                return [LiteralTranslation(**literal_translation) for literal_translation in
                        json.loads(payload.get('body').decode())]
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    async def fetch_response_suggestions(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="response_suggestion-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        response_body = response.get('Payload').read()
        logging.info(f"Received lambda response: {response_body}")
        try:
            payload = json.loads(response_body)
            status_code = payload.get('status_code')
            if status_code == 200:
                return [ResponseSuggestion(**suggestion) for suggestion in json.loads(payload.get('body'))]
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    async def fetch_syntactical_analysis(self, sentence: str, language: str):
        response = self.lambda_client.invoke(
            FunctionName="syntactical_analysis-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence, "language": language})
        )
        response_body = response.get('Payload').read()
        logging.info(f"Received lambda response: {response_body}")
        try:
            payload = json.loads(response_body)
            status_code = payload.get('status_code')
            if status_code == 200:
                return [SyntacticalAnalysis(**a) for a in json.loads(response_body).get('body')]
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")


if __name__ == '__main__':
    import os

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    client = LambdaClient(os.getenv("ACCESS_KEY_ID"),
                          os.getenv("SECRET_ACCESS_KEY"),
                          "eu-central-1")
    logging.info(asyncio.run(client.fetch_literal_translations("Wie viel kostet das Bier?")))
