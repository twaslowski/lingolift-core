from concurrent.futures import ThreadPoolExecutor

from llm.gpt_adapter import openai_exchange
from llm.message import Message
from nlp.syntactical_analysis import perform_analysis
from itertools import product

from nlp.universal_features import get_all_feature_instances
from util.timing import timed


@timed
def retrieve_all_inflections(word: str) -> list[dict]:
    feature_permutations = generate_feature_permutations(word)
    result = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(inflect, word, stringify_feature_permutation(permutation)) for permutation in
                   feature_permutations]
        for future in futures:
            result.append(future.result())
    return result


def inflect(word: str, morphology: str) -> dict:
    prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
    msg = Message(role="user", content=prompt.format(word, morphology))
    result = openai_exchange([msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False)
    return {morphology: result}


def generate_feature_permutations(word: str) -> list[dict]:
    """
    Generates all possible feature instance permutations required for a declined or conjugated word.
    For a declined noun, this would be all possible combinations of Case and Number;
    for a conjugated verb, this would be all possible combinations of Person and Number.
    More features can be added as required, but the amount of permutations grows exponentially and the
    complexity rises drastically, as German conjugations require auxiliary verbs for certain tenses,
    which my custom model does not support yet.
    :param word: The word to generate feature permutations for.
    Required to determine the exact features that should be permuted.
    :return:
    """
    analysis = perform_analysis(word, "DE")[0]  # only analyze one word at a time right now, only support German
    print(analysis)
    pos_tag = analysis.pos.value
    match pos_tag:
        # define features on which to iterate
        case "NOUN":
            features = ["Case", "Number"]
        case "VERB":
            features = ["Person", "Number"]
        case _:
            return []
    # magical chatgpt code
    feature_instances_list = [get_all_feature_instances(feature) for feature in features]
    permutations = list(product(*feature_instances_list))
    result = []
    for values in permutations:
        feature_permutation = dict(zip(features, values))
        result.append(feature_permutation)
    return result


# duplicate from shared/model/syntactical_analysis.py
def stringify_feature_permutation(permutation: dict) -> str:
    return '|'.join([f'{k}={v}' for k, v in permutation.items()])


if __name__ == '__main__':
    print(retrieve_all_inflections("gehen"))
