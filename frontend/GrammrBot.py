import asyncio
import logging
import sys
import time
from asyncio import create_task

import streamlit as st
from shared.client import Client
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.response_suggestion import should_generate_response_suggestions  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]
from shared.model.translation import Translation  # type: ignore[import-untyped]
from shared.rendering import Stringifier, MarkupLanguage
from shared.exception import ApplicationException


def create_client(use_local: bool = False) -> Client:
    if use_local:
        return Client(host="http://localhost:5001")
    else:
        api_gateway_url = st.secrets["API_GATEWAY"]
        return Client(host=api_gateway_url)


async def chat(client: Client, stringifier: Stringifier):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append(
            {"role": "assistant", "content": stringifier.introductory_text()}
        )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What should I translate for you?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with (st.chat_message("assistant")):
            sentence = find_latest_user_message(st.session_state.messages)["content"]

            # create futures for all requests
            translation_future = create_task(client.fetch_translation(sentence))
            if should_fetch_response_suggestions := should_generate_response_suggestions(
                sentence
            ):
                response_suggestions = create_task(
                    client.fetch_response_suggestions(sentence)
                )
            syntactical_translations_future = create_task(
                client.fetch_syntactical_analysis(sentence)
            )
            literal_translations_future = create_task(
                client.fetch_literal_translations(sentence)
            )
            try:
                # render translation
                with st.spinner("Translating"):
                    translation = await translation_future
                translation_stringified = stringifier.stringify_translation(
                    sentence, translation
                )
                render_message(translation_stringified, 0.025)

                # render syntactical analysis
                with st.spinner("Fetching syntactical analysis ..."):
                    analysis = await syntactical_translations_future
                    literal_translation = await literal_translations_future
                analysis_stringified = stringifier.coalesce_analyses(
                    literal_translation, analysis
                )
                render_message(analysis_stringified)

                # optionally render response suggestions
                if should_fetch_response_suggestions:
                    with st.spinner("Fetching suggestions ..."):
                        await response_suggestions
                    response_suggestions_stringified = (
                        stringifier.stringify_suggestions(response_suggestions.result())
                    )
                    render_message(response_suggestions_stringified)

            # exception handling
            except ApplicationException as e:
                st.error(e.error_message)
            except Exception as e:
                logging.error(f"Error: {e}")
                st.error("An unexpected error has occurred.")


def find_latest_user_message(messages: list) -> dict[str, str]:
    """
    Filters all messages in the session state and returns the latest message with message['role'] == 'user'
    :param messages: st.session_state.messages
    :return: latest user message
    """
    user_messages = [message for message in messages if message["role"] == "user"]
    if len(user_messages) > 0:
        return user_messages[-1]
    else:
        return {}


def render_message(string: str, interval: float = 0.025, placeholder=None) -> None:
    if not placeholder:
        placeholder = st.empty()
    for i in range(len(string)):
        placeholder.markdown(string[:i] + "▌")
        time.sleep(interval)
    placeholder.markdown(string)
    st.session_state.messages.append({"role": "assistant", "content": string})


def parse_args():
    args = sys.argv
    if "local" in args:
        return True


if __name__ == "__main__":
    local = parse_args()
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    st.set_page_config(page_title="GrammrBot")
    client = create_client(use_local=local)
    stringifier = Stringifier(MarkupLanguage.MARKDOWN)
    asyncio.run(chat(client, stringifier))
