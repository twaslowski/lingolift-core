import json
from typing import Optional

from shared.exception import ApplicationException


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


def check_pre_warm(event: dict[str, str]) -> Optional[dict]:
    # todo refactor this
    # should be two separate functions is_pre_warm and return_pre_warm with a static response value
    body = json.loads(event.get("body", "{}"))
    if body.get("pre_warm") is not None:
        return ok({"pre-warmed": "true"})
    return None
