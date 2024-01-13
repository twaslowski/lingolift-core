import asyncio
import base64

import requests  # type: ignore[import-untyped]
import streamlit as st
import time
from shared.model.error import LingoliftError  # type: ignore[import-untyped]
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.response_suggestion import ResponseSuggestion  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]
from shared.model.translation import Translation  # type: ignore[import-untyped]

TITLE = "lingolift"


async def main() -> None:
    st.title(TITLE)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What should I translate for you?"):
        # Add user message to chat history
        # todo this can be refactored to use the Message class from backend
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            render_message("Translating ...", 0.05)
            sentence = find_latest_user_message(st.session_state.messages)['content']
            translation = fetch_translation(sentence)
            render_message(stringify_translation(sentence, translation), 0.025)

            gif_md = display_loading_gif()
            async with asyncio.TaskGroup() as tg:
                suggestions = await tg.create_task(fetch_suggestions(sentence))
                literal_translations = await tg.create_task(fetch_literal_translations(sentence))
                syntactical_analysis = await tg.create_task(
                    fetch_syntactical_analysis(sentence, translation.language))

            gif_md.empty()
            analysis_rendered = coalesce_analyses(literal_translations, syntactical_analysis)
            render_message(suggestions, 0.025)
            render_message(analysis_rendered, 0.025)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": translation})


async def render_loading_placeholder(interval: float, event: asyncio.Event):
    placeholder = st.empty()
    while not event.is_set():
        placeholder.markdown("▌")
        await asyncio.sleep(interval * 2)
        placeholder.markdown("")
        await asyncio.sleep(interval * 2)


def fetch_translation(sentence: str) -> Translation | LingoliftError:
    print(f"fetching translation for sentence '{sentence}'")
    response = requests.post("http://localhost:5001/translation", json={"sentence": sentence})
    print(f"received translation for sentence '{sentence}': '{response}'")
    if response.status_code != 200:
        return LingoliftError(**response.json())
    else:
        return Translation(**response.json())


def stringify_translation(sentence: str, translation: Translation) -> str:
    return f"### Translation\n\n" \
           f"'*{sentence}*' is {translation.language} and translates to '*{translation.translation}*'"


async def fetch_suggestions(sentence: str) -> str:
    response = requests.post("http://localhost:5001/response-suggestion", json={"sentence": sentence}).json()
    print(f"Received suggestions for sentence '{sentence}': '{response}'")
    response_string = "### Response suggestions\n\n"
    response_suggestions = [ResponseSuggestion(**r) for r in response]
    for suggestion in response_suggestions:
        response_string += f"*'{suggestion.suggestion}'*\n\n"
        response_string += f"{suggestion.translation}\n\n"
    return response_string


async def fetch_literal_translations(sentence: str) -> list[LiteralTranslation] | LingoliftError:
    response = requests.post("http://localhost:5001/literal-translation", json={"sentence": sentence})
    if response.status_code != 200:
        return LingoliftError(**response.json())
    else:
        response = response.json()
        print(f"Received literal translations for sentence '{sentence}': '{response}'")
        return [LiteralTranslation(**literal_translation) for literal_translation in response]


async def fetch_syntactical_analysis(sentence: str, language: str) -> list[SyntacticalAnalysis] | LingoliftError:
    response = requests.post("http://localhost:5001/syntactical-analysis",
                             json={"sentence": sentence,
                                   "language": language})
    if response.status_code != 200:
        return LingoliftError(**response.json())
    else:
        response = response.json()
        print(f"Received syntactical analysis for sentence '{sentence}': '{response}'")
        return [SyntacticalAnalysis(**syntactical_analysis) for syntactical_analysis in response]


def coalesce_analyses(literal_translations: list[LiteralTranslation] | LingoliftError,
                      syntactical_analysis: list[SyntacticalAnalysis] | LingoliftError) -> str:
    """
    If both a literal translation of the words in the sentence and the syntactical analysis (i.e. part-of-speech
    tagging) are available, they get coalesced in this function, meaning each word gets displayed alongside its
    translation and its morphological features. If only the literal translation is available, the translations
    are displayed. If neither or only the morphological analysis is available, the function returns an error message.
    :param literal_translations:
    :param syntactical_analysis:
    :return:
    """
    if type(literal_translations) == LingoliftError:
        return f"The analysis failed: {literal_translations.error_message}"
    response_string = "### Vocabulary and Grammar breakdown\n\n"
    if type(syntactical_analysis) == LingoliftError:
        response_string += f"Morphological analysis failed: {syntactical_analysis.error_message}; " \
                           f"however, the literal translation is available.\n\n"
    for word in literal_translations:
        word_analysis = find_analysis(word.word, syntactical_analysis)
        response_string += f"*{word.word}*: {word.translation}"
        if word_analysis:
            response_string += f" (lemma: {word_analysis.lemma}, " \
                               f"morphology {word_analysis.morphology}, " \
                               f"dependencies: {word_analysis.dependencies})\n\n"
        else:
            response_string += "\n\n"
    return response_string


def find_analysis(word: str, syntactical_analyses: list[SyntacticalAnalysis]) -> SyntacticalAnalysis | None:
    """
    :param word: Word from the literal translation
    :param syntactical_analyses: Set of syntactical analyses for words in the sentence
    :return: The analysis for the word including the lemma, dependencies and morphology, if available.
    """
    if type(syntactical_analyses) == LingoliftError:
        return None
    for analysis in syntactical_analyses:
        if analysis.word == word and analysis.morphology != '':
            return analysis
    return None


def find_latest_user_message(messages: list) -> dict[str, str]:
    """
    Filters all messages in the session state and returns the latest message with message['role'] == 'user'
    :param messages: st.session_state.messages
    :return: latest user message
    """
    user_messages = [message for message in messages if message['role'] == 'user']
    if len(user_messages) > 0:
        return user_messages[-1]
    else:
        return {}


def render_message(string: str, interval: float):
    placeholder = st.empty()
    for i in range(len(string)):
        placeholder.markdown(string[:i] + "▌")
        time.sleep(interval)
    placeholder.markdown(string)


def display_loading_gif():
    """### gif from local file"""
    file_ = open("resources/loading.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    return st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" height=30px alt="loading gif">',
        unsafe_allow_html=True,
    )


if __name__ == '__main__':
    asyncio.run(main())
