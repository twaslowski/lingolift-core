# Assume the role and obtain temporary credentials
import boto3


def assume_role(role_arn: str, external_id: str):
    sts_client = boto3.client('sts')

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='ExternalSession',
        ExternalId=external_id
    )

    credentials = response['Credentials']
    return credentials


def get_secret(credentials, secret_name: str):
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    secrets_manager_client = session.client('secretsmanager')
    response = secrets_manager_client.get_secret_value(SecretId=secret_name)

    secret_value = response['SecretString']
    return secret_value
