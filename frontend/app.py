import asyncio
import logging
import time

import requests  # type: ignore[import-untyped]
import streamlit as st
from shared.client import Client
from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.response_suggestion import ResponseSuggestion  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]
from shared.model.translation import Translation  # type: ignore[import-untyped]
from shared.rendering import Stringifier, MarkupLanguage

TITLE = "grammr"


async def main() -> None:
    st.title(TITLE)

    backend_protocol = st.secrets.connection.protocol
    backend_host = st.secrets.connection.host
    backend_port = st.secrets.connection.port
    client = Client(backend_protocol, backend_host, backend_port)
    stringifier = Stringifier(MarkupLanguage.MARKDOWN)

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
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # the syntactical analysis only ever happens when the translation has been fetched successfully
        translation = None

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            try:
                with st.spinner("Translating"):
                    sentence = find_latest_user_message(st.session_state.messages)['content']
                    translation = await client.fetch_translation(sentence)
                translation_stringified = stringifier.stringify_translation(sentence, translation)
                render_message(translation_stringified, 0.025)
                st.session_state.messages.append({"role": "assistant", "content": translation_stringified})
            except ApplicationException as e:
                st.error(e.error_message)
            # broader exception clause not covered in client, e.g. if client is entirely unreachable
            except Exception as e:
                logging.error("Error: ", e)
                st.error("An unexpected error has occurred.")

        if translation is not None:
            with st.chat_message("assistant"):
                try:
                    with st.spinner("Fetching suggestions and syntactical analysis ..."):
                        suggestions, literal_translations, syntactical_analysis = await asyncio.gather(
                            client.fetch_response_suggestions(sentence),
                            client.fetch_literal_translations(sentence),
                            client.fetch_syntactical_analysis(sentence, translation.language_code),
                            return_exceptions=True)

                    # stringify analysis, literal translation and suggestions
                    analysis_stringified = stringifier.coalesce_analyses(literal_translations, syntactical_analysis)
                    response_suggestions_stringified = stringifier.stringify_suggestions(suggestions)

                    # render them to the chat
                    render_message(analysis_stringified, 0.025)
                    render_message(response_suggestions_stringified, 0.025)

                    # add messages to chat history
                    st.session_state.messages.append({"role": "assistant", "content": analysis_stringified})
                    st.session_state.messages.append({"role": "assistant", "content": response_suggestions_stringified})
                except ApplicationException as e:
                    st.error(e.error_message)
                except Exception as e:
                    logging.error("Error: ", e)
                    st.error("An unexpected error has occurred.")


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


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    asyncio.run(main())
