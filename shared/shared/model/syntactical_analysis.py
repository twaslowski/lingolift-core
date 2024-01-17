from pydantic import BaseModel


class SyntacticalAnalysis(BaseModel):
    word: str
    morphology: str
    lemma: str
    pos: str
    dependency: str
    pos_explanation: str

    def stringify_lemma(self) -> str:
        if self.word.lower() != self.lemma.lower():
            return f' (from: {self.lemma})'
        else:
            return ''

    def stringify_morphology(self) -> str:
        if self.morphology != '':
            return f'Morphological features: {self.morphology}'
        else:
            return ''

    def stringify(self) -> str:
        features = []
        add_feature(features, self.stringify_lemma())
        add_feature(features, self.pos_explanation)
        add_feature(features, self.stringify_morphology())
        return '; '.join(features)


def add_feature(features: list[str], feature: str):
    if feature != '':
        features.append(feature)
