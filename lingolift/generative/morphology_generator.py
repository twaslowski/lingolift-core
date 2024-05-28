from shared.model.inflection import Inflection

from lingolift.generative.abstract_generator import AbstractGenerator
from lingolift.llm.gpt_adapter import GPTAdapter
from lingolift.llm.message import Message


class MorphologyGenerator(AbstractGenerator):
    def __init__(self, gpt_adapter: GPTAdapter):
        super().__init__(gpt_adapter)

    def inflect(self, word: str, morphology: dict[str, str]) -> Inflection:
        prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
        msg = Message(
            role="user",
            content=prompt.format(word, self.stringify_morphology(morphology)),
        )
        result = self.gpt_adapter.openai_exchange(
            [msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False
        )
        return Inflection(**{"word": result, "morphology": morphology})

    # duplicate from shared/model/syntactical_analysis.py
    @staticmethod
    def stringify_morphology(permutation: dict) -> str:
        return "|".join([f"{k}={v}" for k, v in permutation.items()])
