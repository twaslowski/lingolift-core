import asyncio

import streamlit as st
from GrammrBot import create_client
from shared.rendering import Stringifier, MarkupLanguage


async def inflectable():
    client = create_client(use_local=True)
    stringifier = Stringifier(MarkupLanguage.MARKDOWN)
    word = st.text_input("Enter a word")

    if word:
        inflections = await client.fetch_inflections(word)
        table = markdown_table()
        for inflection in inflections:
            case = inflection.morphology.get('Case').upper()
            number = inflection.morphology.get('Number').upper()
            replacement_string = f"${case}${number}"
            print(replacement_string)
            table = table.replace(replacement_string, inflection.word)
        st.markdown(table)


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
