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
        return response


if __name__ == '__main__':
    client = LambdaClient("AKIATS5FQL45YHEW4FR2", "DW1yxaBDVT8URxfgzBm8th7ZFpYRjClRtauAst3W", "eu-central-1")
    print(client.fetch_translation("Wie viel kostet ein Bier?"))

