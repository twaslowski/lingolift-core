import json

import pytest

from lingolift.util.lambda_proxy_return import check_pre_warm


@pytest.fixture
def pre_warm_event():
    return {"body": '{ "pre_warm": "true" }'}


@pytest.fixture
def regular_event():
    return {"body": '{ "word": "test" }'}


def test_should_return_none_for_regular_event(regular_event):
    assert check_pre_warm(regular_event) is None


def test_should_return_pre_warm_response(pre_warm_event):
    assert json.loads(check_pre_warm(pre_warm_event)["body"])["pre-warmed"] == "true"
