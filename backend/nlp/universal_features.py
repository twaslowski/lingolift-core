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


feature_types = {
    'Case': Case,
    'Number': Number,
    'Gender': Gender,
}


def convert(tags: list[str]) -> str:
    tag_values = {feature: None for feature in feature_types}

    # Parse and store the tag values
    for tag in tags:
        key, value = tag.split('=')
        value = value.upper()
        feature_type = feature_types.get(key)
        if feature_type and hasattr(feature_type, value):
            tag_values[key] = feature_type[value].value

    readable_tags = [tag_values[feature] for feature in feature_types if tag_values[feature]]
    return ' '.join(readable_tags)
