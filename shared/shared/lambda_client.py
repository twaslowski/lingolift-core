import json
import logging

import boto3

from shared.exception import ApplicationException
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

    def fetch_translation(self, sentence: str) -> Translation:
        response = self.lambda_client.invoke(
            FunctionName="translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        response_body = response.get('Payload').read()
        logging.info(f"Received lambda response: {response_body}")
        # todo this is very rudimentary exception handling
        # The status code solution specifically is very rough. An introduction of an API Gateway would make this easier.
        try:
            payload = json.loads(response_body)
            status_code = payload.get('status_code')
            if status_code == 200:
                return Translation(**payload.get('body'))
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    def fetch_literal_translations(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="literal_translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        print(response.get('Payload').read())
        try:
            payload = json.loads(response['Payload'].read())
            status_code = payload.get('status_code')
            if status_code == 200:
                return [LiteralTranslation(**literal_translation) for literal_translation in payload.get('body')]
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    def fetch_response_suggestions(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="respoonse_suggestion-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        print(response.get('Payload').read())
        try:
            payload = json.loads(response['Payload'].read())
            status_code = payload.get('status_code')
            if status_code == 200:
                return [ResponseSuggestion(**suggestion) for suggestion in payload.get('body')]
            else:
                raise ApplicationException(**payload.get('body'))
        except json.JSONDecodeError:
            raise ApplicationException("Could not parse response from backend.")
        except Exception:
            raise ApplicationException("Unknown error occurred.")

    def fetch_syntactical_analysis(self, sentence: str, language: str):
        raise ApplicationException("Not implemented yet.")
