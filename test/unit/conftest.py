import pytest

from lingolift.llm.gpt_adapter import GPTAdapter


@pytest.fixture
def openai_adapter() -> GPTAdapter:
    adapter = GPTAdapter(api_key="some-token", base_url="http://localhost:5002/v1/")
    return adapter
