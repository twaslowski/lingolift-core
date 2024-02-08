import asyncio
import logging
import os
import sys
from typing import Tuple

import streamlit as st
from shared.exception import ApplicationException
from shared.model.inflection import Inflections, Inflection

from GrammrBot import create_client


async def inflectable():
    """
    The main function representing the inflection table for arbitrary German words.
    :return:
    """
    word = st.text_input("Enter a word")
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


def create_verb_table(inflections: list[Inflection]) -> str:
    table_template = (
        "| Person    | Singular          | Plural      |\n"
        "|-----------|-------------------|-------------|\n"
        "| 1. Person | ich $1$SING       | wir $1$PLUR |\n"
        "| 2. Person | du $2$SING        | ihr $2$PLUR |\n"
        "| 3. Person | er/sie/es $3$SING | sie $3$PLUR |"
    )
    for inflection in inflections:
        person = inflection.morphology.get("Person").upper()
        number = inflection.morphology.get("Number").upper()
        replacement_string = f"${person}${number}"
        table_template = table_template.replace(replacement_string, inflection.word)
    return table_template


def create_noun_table(inflections: list[Inflection]) -> str:
    table_template = (
        "| Casus      | Singular  | Plural    |\n"
        "|------------|-----------|-----------|\n"
        "| Nominativ  | $NOM$SING | $NOM$PLUR |\n"
        "| Genitiv    | $GEN$SING | $GEN$PLUR |\n"
        "| Dativ      | $DAT$SING | $DAT$PLUR |\n"
        "| Akkusative | $ACC$SING | $ACC$PLUR |"
    )
    for inflection in inflections:
        case = inflection.morphology.get("Case").upper()
        number = inflection.morphology.get("Number").upper()
        replacement_string = f"${case}${number}"
        table_template = table_template.replace(replacement_string, inflection.word)
    return table_template


def create_inflections_table(inflections: Inflections) -> str:
    pos = inflections.pos.value
    if pos == "VERB" or pos == "AUX":
        return create_verb_table(inflections.inflections)
    if pos == "NOUN" or pos == "ADJ":
        return create_noun_table(inflections.inflections)
    else:
        raise ApplicationException(
            f"Generating inflections for word type {inflections.pos.explanation} is not supported yet."
        )


if __name__ == "__main__":
    local = "local" in sys.argv
    client = create_client(local)
    asyncio.run(inflectable())
