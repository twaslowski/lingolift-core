import pytest

from lingolift.generative.morphology_generator import MorphologyGenerator
from lingolift.llm.gpt_adapter import GPTAdapter
from lingolift.nlp.morphologizer import Morphologizer


@pytest.fixture
def gpt_adapter() -> GPTAdapter:
    adapter = GPTAdapter(api_key="some-token", base_url="http://localhost:5002/v1/")
    return adapter


@pytest.fixture
def morphology_generator(gpt_adapter):
    return MorphologyGenerator(gpt_adapter)


@pytest.fixture
def morphologizer(morphology_generator) -> Morphologizer:
    return Morphologizer(morphology_generator)
