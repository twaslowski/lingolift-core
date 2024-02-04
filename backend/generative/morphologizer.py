from llm.gpt_adapter import openai_exchange
from llm.message import Message
from nlp.syntactical_analysis import pos_tags_to_dict, perform_analysis

import spacy

from nlp.universal_features import get_all_feature_instances, nominal_features, verbal_features


def retrieve_inflections(word: str) -> dict:
    analysis = perform_analysis(word, "DE")[0]  # only analyze one word at a time right now
    pos_tag = analysis.pos.value
    match pos_tag:
        case "NOUN":
            for feature in nominal_features:
                feature_instances = get_all_feature_instances(feature)  # e.g. "Nom", "Acc", "Dat", "Gen"
                for instance in feature_instances:
                    print(f"{feature}={instance}")
        case "VERB":
            pass
        case _:
            return {}


def inflect(word: str, morphology: str) -> str:
    prompt = "Inflect the following word according to the CoNNL-U Universal Feature Tags: {}, {}"
    msg = Message(role="user", content=prompt.format(word, morphology))
    return openai_exchange([msg], model_name="ft:gpt-3.5-turbo-1106:tobiorg::8npM4Pcf", json_mode=False)


def get_instances_for_features(features: dict) -> list[str]:
    """
    :param feature: The feature to get all instances for, e.g. "Case"
    :return: A list of all instances for the given feature, e.g. "Nom", "Acc", "Dat", "Gen"
    """
    for feature in features.keys():
        get_all_feature_instances(feature)


if __name__ == '__main__':
    retrieve_inflections("Hund")
