import asyncio

import streamlit as st
from shared.exception import ApplicationException

from GrammrBot import create_client


async def inflectable():
    client = create_client()
    # stringifier = Stringifier(MarkupLanguage.MARKDOWN)
    word = st.text_input("Enter a word")

    if word:
        try:
            inflections = await client.fetch_inflections(word)
            table = markdown_table()
            for inflection in inflections:
                case = inflection.morphology.get('Case').upper()
                number = inflection.morphology.get('Number').upper()
                replacement_string = f"${case}${number}"
                print(replacement_string)
                table = table.replace(replacement_string, inflection.word)
            st.markdown(table)
        except ApplicationException as e:
            st.error(e.error_message)
        except Exception:
            st.error(f"An unexpected error has occurred")


def markdown_table():
    return """
        | Casus      | Singular | Plural |
        |------------|----------|--------|
        | Nominativ  | $NOM$SING         | $NOM$PLUR       |
        | Genitiv    | $GEN$SING         | $GEN$PLUR       |
        | Dativ      | $DAT$SING         | $DAT$PLUR       |
        | Akkusative | $ACC$SING         | $ACC$PLUR       |
        """


if __name__ == '__main__':
    asyncio.run(inflectable())
