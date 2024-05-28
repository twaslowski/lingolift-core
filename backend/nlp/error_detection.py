from typing import Optional

from shared.model.syntactical_analysis import SyntacticalAnalysis

from nlp.syntactical_analysis import perform_analysis


def has_article_mismatch(analysis: list[SyntacticalAnalysis]):
    for word in analysis:
        print(word)
        if word.pos.value == "DET" or word.pos.value == "ART":
            # todo: actually getting the dependency of the word requires additional logic.
            # maybe i should do actual linking of the words in the syntactical analysis?
            dependency = get_dependency(word.word, analysis)
            print(dependency)
            # print(dependency.morphology == word.morphology)  # noqa


def get_dependency(
    word: str, analysis: list[SyntacticalAnalysis]
) -> Optional[SyntacticalAnalysis]:
    for a in analysis:
        if a.word == word:
            return a
    return None


if __name__ == "__main__":
    analysis = perform_analysis("Wie viel kostet eine Bier", "DE")
    has_article_mismatch(analysis)
