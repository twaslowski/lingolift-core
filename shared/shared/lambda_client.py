import json

import boto3


class LambdaClient:
    def __init__(self, access_key_id: str, secret_access_key: str, region: str):
        self.lambda_client = boto3.client(
            'lambda',
            region_name=region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key
        )

    def fetch_translation(self, sentence: str):
        response = self.lambda_client.invoke(
            FunctionName="translation-lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps({"sentence": sentence})
        )
        print(response)
        return json.loads(response['Payload'].read())


if __name__ == '__main__':
    import os
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")
    region = "eu-central-1"
    client = LambdaClient(access_key_id, secret_access_key, region)
    print(client.fetch_translation("askdasd"))
