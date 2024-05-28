from concurrent.futures import ThreadPoolExecutor
from itertools import product

from lingolift.llm.gpt_adapter import openai_exchange
from lingolift.llm.message import Message
from lingolift.nlp.syntactical_analysis import perform_analysis
from shared.model.inflection import Inflection, Inflections
from shared.universal_features import get_all_feature_instances
from lingolift.util.timing import timed


@timed
def retrieve_all_inflections(word: str) -> Inflections:
    # Get the part of speech tag for the word
    analysis = perform_analysis(word, "DE")[
        0
    ]  # only analyze one word at a time right now, only support German
    pos = analysis.pos
    gender = analysis.morphology.tags.get("Gender", None)
    feature_permutations = generate_feature_permutations(pos.value)
    result = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(inflect, word, permutation)
            for permutation in feature_permutations
        ]
        for future in futures:
            result.append(future.result())
    return Inflections(pos=pos, gender=gender, inflections=result)


def inflect(word: str, morphology: dict[str, str]) -> Inflection:
    prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
    msg = Message(
        role="user", content=prompt.format(word, stringify_morphology(morphology))
    )
    result = openai_exchange(
        [msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False
    )
    return Inflection(**{"word": result, "morphology": morphology})


def generate_feature_permutations(pos_tag: str) -> list[dict]:
    """
    Generates all possible feature instance permutations required for a declined or conjugated word.
    For a declined noun, this would be all possible combinations of Case and Number;
    for a conjugated verb, this would be all possible combinations of Person and Number.
    More features can be added as required, but the amount of permutations grows exponentially and the
    complexity rises drastically, as German conjugations require auxiliary verbs for certain tenses,
    which my custom model does not support yet.
    :param pos_tag: VERB | NOUN
    Required to determine the exact features that should be permuted.
    :return:
    """
    match pos_tag:
        # define features on which to iterate
        case "NOUN" | "ADJ":
            features = ["Case", "Number"]
        case "VERB" | "AUX":
            features = ["Person", "Number"]
        case _:
            return []
    # magical chatgpt code
    feature_instances_list = [
        get_all_feature_instances(feature) for feature in features
    ]
    permutations = list(product(*feature_instances_list))
    result = []
    for values in permutations:
        feature_permutation = dict(zip(features, values))
        result.append(feature_permutation)
    return result


# duplicate from shared/model/syntactical_analysis.py
def stringify_morphology(permutation: dict) -> str:
    return "|".join([f"{k}={v}" for k, v in permutation.items()])


if __name__ == "__main__":
    print(retrieve_all_inflections("gehen"))
