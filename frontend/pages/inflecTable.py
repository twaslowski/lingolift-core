import asyncio
import logging
import sys

import streamlit as st
from shared.exception import ApplicationException
from shared.model.inflection import Inflections

from GrammrBot import create_client


async def inflectable():
    """
    The main function representing the inflection table for arbitrary German words.
    :return:
    """
    word = st.text_input("Enter a word")
    st.text("Note: This feature is in beta right now and is very limited.")
    if word:
        try:
            inflections = await client.fetch_inflections(word)
            table = create_inflections_table(inflections)
            st.markdown(table)
        except ApplicationException as e:
            st.error(e.error_message)
        except Exception as e:
            logging.error(f"Error: {e}")
            st.error("An unexpected error has occurred.")


def create_verb_table(inflections: Inflections) -> str:
    table_template = (
        "| Person    | Singular          | Plural      |\n"
        "|-----------|-------------------|-------------|\n"
        "| 1. Person | ich $1$SING       | wir $1$PLUR |\n"
        "| 2. Person | du $2$SING        | ihr $2$PLUR |\n"
        "| 3. Person | er/sie/es $3$SING | sie $3$PLUR |"
    )
    for inflection in inflections.inflections:
        person = inflection.morphology.get("Person").upper()
        number = inflection.morphology.get("Number").upper()
        replacement_string = f"${person}${number}"
        table_template = table_template.replace(replacement_string, inflection.word)
    return table_template


def create_noun_table(inflections: Inflections) -> str:
    table_template = (
        "| Casus      | Singular  | Plural    |\n"
        "|------------|-----------|-----------|\n"
        "| Nominativ  | $ART0 $NOM$SING | $ART4 $NOM$PLUR |\n"
        "| Genitiv    | $ART1 $GEN$SING | $ART5 $GEN$PLUR |\n"
        "| Dativ      | $ART2 $DAT$SING | $ART6 $DAT$PLUR |\n"
        "| Akkusative | $ART3 $ACC$SING | $ART7 $ACC$PLUR |"
    )
    for inflection in inflections.inflections:
        case = inflection.morphology.get("Case").upper()
        number = inflection.morphology.get("Number").upper()
        replacement_string = f"${case}${number}"
        table_template = table_template.replace(replacement_string, inflection.word)
    table_template = add_articles(inflections.gender, table_template)
    return table_template


def add_articles(gender: str, table_template: str):
    for i, article in enumerate(articles(gender.upper())):
        replacement_string = f"$ART{i}"
        table_template = table_template.replace(replacement_string, article)
    return table_template


def articles(gender: str):
    if gender == "MASC":
        return ["der", "des", "dem", "den", "die", "der", "den", "die"]
    if gender == "FEM":
        return ["die", "der", "der", "die", "die", "der", "den", "die"]
    if gender == "NEUT":
        return ["das", "des", "dem", "das", "die", "der", "den", "die"]
    raise ApplicationException(
        f'Gender must be "Masc", "Fem" or "Neut". Given: {gender}'
    )


def create_inflections_table(inflections: Inflections) -> str:
    pos = inflections.pos.value
    if pos == "VERB" or pos == "AUX":
        return create_verb_table(inflections)
    if pos == "NOUN":
        return create_noun_table(inflections)
    else:
        raise ApplicationException(
            f"Generating inflections for word type {inflections.pos.explanation} is not supported yet."
        )


if __name__ == "__main__":
    local = "local" in sys.argv
    client = create_client(local)
    asyncio.run(inflectable())
