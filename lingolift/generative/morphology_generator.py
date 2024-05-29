from shared.model.inflection import Inflection

from lingolift.generative.abstract_generator import AbstractGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.llm.message import Message


class MorphologyGenerator(AbstractGenerator):
    def __init__(self, llm_adapter: AbstractLLMAdapter):
        super().__init__(llm_adapter)

    def inflect(self, word: str, morphology: dict[str, str]) -> Inflection:
        """
        Inflects a word according to the given morphology. For example, the German word "gehen" with the features
        Person=1 Number=1 would yield the inflection "gehe".
        :param word: The word to be inflected.
        :param morphology: The morphology to inflect the word with.
        :return:
        """
        prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
        msg = Message(
            role="user",
            content=prompt.format(word, self.stringify_morphology(morphology)),
        )
        result = self.llm_adapter.exchange(
            [msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False
        )
        return Inflection(**{"word": result, "morphology": morphology})

    # duplicate from shared/model/syntactical_analysis.py
    @staticmethod
    def stringify_morphology(permutation: dict) -> str:
        return "|".join([f"{k}={v}" for k, v in permutation.items()])
