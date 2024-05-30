from lingolift.abstract_context_container import AbstractLambdaContextContainer
from lingolift.generative.inflection_generator import InflectionGenerator
from lingolift.llm.abstract_adapter import AbstractLLMAdapter
from lingolift.nlp.morphologizer import Morphologizer


class NLPLambdaContextContainer(AbstractLambdaContextContainer):
    llm_adapter: AbstractLLMAdapter
    morphology_generator: InflectionGenerator
    morphologizer: Morphologizer

    def __init__(self, llm_adapter: AbstractLLMAdapter = None):
        super().__init__(llm_adapter)
        self.morphology_generator = InflectionGenerator(self.llm_adapter)
        self.morphologizer = Morphologizer(self.morphology_generator)
