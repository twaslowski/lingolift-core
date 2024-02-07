import asyncio
import logging
import sys
from typing import Tuple

import streamlit as st
from shared.exception import ApplicationException
from shared.model.inflection import Inflections

from GrammrBot import create_client


def extract_additional_features(inflections: Inflections) -> Tuple[str, list[str], list[str]]:
    if inflections.pos == 'NOUN' or inflections.pos == 'ADJ':
        return 'Case', ['Nominativ', 'Genitiv', 'Dativ', 'Akkusativ'], ['Nom', 'Gen', 'Dat', 'Acc']
    if inflections.pos == 'VERB' or inflections.pos == 'AUX':
        return 'Person', ['1. Person', '2. Person', '3. Person'], ['1', '2', '3']
    else:
        raise ApplicationException(f'Generating inflections for word type {inflections.pos} is not supported yet.')


async def inflectable():
    """
    The main function representing the inflection table for arbitrary German words.
    # todo: The string manipulation here is atrocious. It works; next, make it pretty.
    :return:
    """

    # stringifier = Stringifier(MarkupLanguage.MARKDOWN)
    word = st.text_input("Enter a word")

    if word:
        try:
            inflections = await client.fetch_inflections(word)
            feature_type, feature_instances, placeholders = extract_additional_features(inflections)
            table = markdown_table()
            table = table.replace('$FEAT', feature_type).strip()
            for instance, placeholder in zip(feature_instances, placeholders):
                table += f'\n| {instance} | ${placeholder}$Sing | ${placeholder}$Plur |'
            for inflection in inflections.inflections:
                replacement_string = ''.join([f"${value}" for key, value in sorted(inflection.morphology.items())])
                # if replacement string is formed $Sing$1 instead of $1$Sing, swap the arguments
                if replacement_string[:5] == '$Sing':
                    replacement_string = replacement_string[5:] + replacement_string[:5]
                if replacement_string[:5] == '$Plur':
                    replacement_string = replacement_string[5:] + replacement_string[:5]
                print(replacement_string)
                table = table.replace(replacement_string, inflection.word)
            st.markdown(table)
        except ApplicationException as e:
            st.error(e.error_message)
        except Exception as e:
            logging.error(f"Error: {e}")
            st.error("An unexpected error has occurred.")


def markdown_table():
    return "| $FEAT      | Singular | Plural |\n" \
           "|------------|----------|--------|"


if __name__ == '__main__':
    local = 'local' in sys.argv
    client = create_client(local)
    asyncio.run(inflectable())
