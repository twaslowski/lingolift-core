from shared.exception import ApplicationException
import json


def ok(res: dict | list) -> dict:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(res),
    }


def fail(e: ApplicationException, status: int) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(e.dict()),
    }


def check_pre_warm(event: dict) -> dict:
    body = json.loads(event.get("body"))
    if body.get("pre_warm") is not None:
        return ok({"pre-warmed": "true"})
