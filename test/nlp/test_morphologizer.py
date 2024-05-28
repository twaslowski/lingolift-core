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


def test_feature_permutations_for_non_supported_pos_tag(morphologizer):
    permutations = morphologizer._generate_feature_permutations("non-supported-pos-tag")
    assert permutations == []


def test_feature_permutations_for_noun(morphologizer):
    permutations = morphologizer._generate_feature_permutations("NOUN")
    # 4 cases x 2 numbers = 8 permutations
    assert len(permutations) == 8


def test_feature_permutations_for_verb(morphologizer):
    permutations = morphologizer._generate_feature_permutations("VERB")
    # 3 persons x 2 numbers = 6 permutations
    assert len(permutations) == 6
