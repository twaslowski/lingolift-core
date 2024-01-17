import asyncio
import base64
import time
from typing import Union, Optional

import requests  # type: ignore[import-untyped]
import streamlit as st
from shared.client import Client
from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.response_suggestion import ResponseSuggestion  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]
from shared.model.translation import Translation  # type: ignore[import-untyped]

TITLE = "grammr"


async def main() -> None:
    st.title(TITLE)

    backend_protocol = st.secrets.connection.protocol
    backend_host = st.secrets.connection.host
    backend_port = st.secrets.connection.port
    client = Client(backend_protocol, backend_host, backend_port)

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

        # todo this whole flow has to be refactored, with *proper* error handling. fuck me.
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Translating"):
                try:
                    sentence = find_latest_user_message(st.session_state.messages)['content']
                    translation = await client.fetch_translation(sentence)
                    render_message(stringify_translation(sentence, translation), 0.025)
                except ApplicationException as e:
                    st.error(e.error_message)
                except Exception:
                    st.error("An unexpected error has occurred.")

        #     with st.spinner("Fetching suggestions and syntactical analysis ..."):
        #         try:
        #             suggestions, literal_translations, syntactical_analysis = await asyncio.gather(
        #                 client.fetch_response_suggestions(sentence),
        #                 client.fetch_literal_translations(sentence),
        #                 client.fetch_syntactical_analysis(sentence, translation.language_code))
        #         except Exception as e:
        #             render_message(f"An error occurred: {e}", 0.025)
        #
        # render_message(stringify_response_suggestions(suggestions), 0.025)
        # analysis_rendered = coalesce_analyses(literal_translations, syntactical_analysis)
        # render_message(analysis_rendered, 0.025)
        #
        # # Add assistant response to chat history
        # st.session_state.messages.append({"role": "assistant", "content": translation})
        # st.session_state.messages.append({"role": "assistant", "content": suggestions})


async def render_loading_placeholder(interval: float, event: asyncio.Event):
    placeholder = st.empty()
    while not event.is_set():
        placeholder.markdown("▌")
        await asyncio.sleep(interval * 2)
        placeholder.markdown("")
        await asyncio.sleep(interval * 2)


def stringify_translation(sentence: str, translation: Translation) -> str:
    return f"### Translation\n\n" \
           f"'*{sentence}*' is {translation.language_name.capitalize()} and translates to '*{translation.translation}*'"


def stringify_response_suggestions(response_suggestions: list[ResponseSuggestion]) -> str:
    response_string = "### Response suggestions\n\n"
    for suggestion in response_suggestions:
        response_string += f"*'{suggestion.suggestion}'*\n\n"
        response_string += f"{suggestion.translation}\n\n"
    return response_string


async def fetch_literal_translations(sentence: str) -> Union[list[LiteralTranslation], ApplicationException]:
    response = requests.post("http://localhost:5001/literal-translation", json={"sentence": sentence})
    if response.status_code != 200:
        return ApplicationException(**response.json())
    else:
        response = response.json()
        print(f"Received literal translations for sentence '{sentence}': '{response}'")
        return [LiteralTranslation(**literal_translation) for literal_translation in response]


async def fetch_syntactical_analysis(sentence: str, language: str) -> Union[
    list[SyntacticalAnalysis], ApplicationException]:
    response = requests.post("http://localhost:5001/syntactical-analysis",
                             json={"sentence": sentence,
                                   "language": language})
    if response.status_code != 200:
        return ApplicationException(**response.json())
    else:
        response = response.json()
        print(f"Received syntactical analysis for sentence '{sentence}': '{response}'")
        return [SyntacticalAnalysis(**syntactical_analysis) for syntactical_analysis in response]


def coalesce_analyses(literal_translations: Union[list[LiteralTranslation], ApplicationException],
                      syntactical_analysis: Union[list[SyntacticalAnalysis], ApplicationException]) -> str:
    """
    If both a literal translation of the words in the sentence and the syntactical analysis (i.e. part-of-speech
    tagging) are available, they get coalesced in this function, meaning each word gets displayed alongside its
    translation and its morphological features. If only the literal translation is available, the translations
    are displayed. If neither or only the morphological analysis is available, the function returns an error message.
    # todo this function is a mess, i need to come up with a smarter way of doing this
    # potentially including a stringify() method in the SyntacticalAnalysis class might be a solution
    :param literal_translations:
    :param syntactical_analysis:
    :return:
    """
    if type(literal_translations) == ApplicationException:
        return f"The analysis failed: {literal_translations.error_message}"
    response_string = "### Vocabulary and Grammar breakdown\n\n"
    if type(syntactical_analysis) == ApplicationException:
        response_string += f"Morphological analysis failed: {syntactical_analysis.error_message}; " \
                           f"however, the literal translation is available.\n\n"
    for word in literal_translations:
        analysis = find_analysis(word.word, syntactical_analysis)
        response_string += f"*{word.word}*: {word.translation}"
        if analysis:
            if analysis.lemma.lower() != analysis.word.lower():
                response_string += f" (from {analysis.lemma}), "
            else:
                response_string += ", "
            response_string += f"{analysis.pos_explanation}"
            if analysis.morphology != "":
                response_string += f"; "
                response_string += f"{analysis.morphology}\n\n"
            else:
                response_string += "\n\n"
        else:
            response_string += "\n\n"
    return response_string


def find_analysis(word: str, syntactical_analyses: list[SyntacticalAnalysis]) -> Optional[SyntacticalAnalysis]:
    """
    :param word: Word from the literal translation
    :param syntactical_analyses: Set of syntactical analyses for words in the sentence
    :return: The analysis for the word including the lemma, dependencies and morphology, if available.
    """
    if type(syntactical_analyses) == ApplicationException:
        return None
    for analysis in syntactical_analyses:
        if analysis.word == word:
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
