from enum import Enum


class Gender(Enum):
    MASC = "Masculine"
    FEM = "Feminine"
    NEUT = "Neuter"
    COM = "Common Gender"


class Number(Enum):
    SING = "Singular"
    PLUR = "Plural"


class Case(Enum):
    NOM = "Nominative"
    GEN = "Genitive"
    DAT = "Dative"
    ACC = "Accusative"
    ABS = "Absolutive"
    ERG = "Ergative"
    VOC = "Vocative"
    INS = "Instrumental"
    DIS = "Distributive"
    CAU = "Causative"
    CMP = "Comparative"
    EQU = "Equative"


class Person(Enum):
    # A 0th person exists in Finnish, a 4th in Navajo. Might support that at some point in the future.
    P1 = "1st person"
    P2 = "2nd person"
    P3 = "3rd person"


class Tense(Enum):
    FUT = "Future tense"
    PRES = "Present tense"
    IMP = "Imperfect"
    PAST = "Past tense"
    PQP = "Pluperfect"


NOUN_FEATURE_SET = {
    'Case': Case,
    'Number': Number,
    'Gender': Gender,
}

VERB_FEATURE_SET = {
    'Person': Person,
    'Number': Number,
    'Tense': Tense
}


def convert(tags: list[str], feature_set: dict) -> str:
    tag_values = {feature: None for feature in feature_set}

    # Parse and store the tag values
    for tag in tags:
        key, value = tag.split('=')
        # This is a very hacky solution. Basically the value here is just '3', which is not a valid Enum key.
        # I've therefore decided to make the Enum key 'P3', but I need to append the 'P' here.
        if key == 'Person':
            value = f'P{value}'
        value = value.upper()
        print(key, value)
        feature_type = feature_set.get(key)
        if feature_type and hasattr(feature_type, value):
            tag_values[key] = feature_type[value].value

    readable_tags = [tag_values[feature] for feature in feature_set if tag_values[feature]]
    return ' '.join(readable_tags)
