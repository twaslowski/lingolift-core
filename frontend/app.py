import asyncio
import logging
import time

import requests  # type: ignore[import-untyped]
import streamlit as st
from shared.lambda_client import LambdaClient
from shared.exception import ApplicationException
from shared.model.literal_translation import LiteralTranslation  # type: ignore[import-untyped]
from shared.model.response_suggestion import should_generate_response_suggestions  # type: ignore[import-untyped]
from shared.model.syntactical_analysis import SyntacticalAnalysis  # type: ignore[import-untyped]
from shared.model.translation import Translation  # type: ignore[import-untyped]
from shared.rendering import Stringifier, MarkupLanguage

TITLE = "grammr"


async def main() -> None:
    access_key_id = st.secrets["ACCESS_KEY_ID"]
    secret_access_key = st.secrets["SECRET_ACCESS_KEY"]
    region = st.secrets["AWS_REGION"]
    client = LambdaClient(access_key_id, secret_access_key, region)
    stringifier = Stringifier(MarkupLanguage.MARKDOWN)

    if await backend_is_healthy(client):
        st.title(TITLE)
        await chat(client, stringifier)
    else:
        st.error("The backend is not available. Please try again later.")
    # st.markdown(stringifier.disclaimer())


async def chat(client: LambdaClient, stringifier: Stringifier):
    intro = st.markdown(stringifier.introductory_text())

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What should I translate for you?"):
        intro.empty()
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
                render_message(translation_stringified)
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
                        generate_suggestions = should_generate_response_suggestions(sentence, translation.translation)
                        # determine if suggestions should be generated in the first place
                        if generate_suggestions:
                            suggestions_future = asyncio.create_task(client.fetch_response_suggestions(sentence))

                        # fetch literal translations and syntactical analysis in parallel
                        literal_translations, syntactical_analysis = await asyncio.gather(
                            client.fetch_literal_translations(sentence),
                            client.fetch_syntactical_analysis(sentence, translation.language_code),
                            return_exceptions=True)

                    if isinstance(literal_translations, ApplicationException):
                        st.error("An unexpected error occurred while fetching literal translations.")

                    # render syntactical analysis
                    analysis_stringified = stringifier.coalesce_analyses(literal_translations, syntactical_analysis)
                    render_message(analysis_stringified)

                    # at this point, the suggestions should be available
                    if generate_suggestions:
                        suggestions = await suggestions_future
                        response_suggestions_stringified = stringifier.stringify_suggestions(suggestions)
                        render_message(response_suggestions_stringified)
                    else:
                        render_message("Your sentence does not appear to be a question; "
                                       "therefore, no response suggestions will be generated.")

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


def render_message(string: str, interval: float = 0.025):
    placeholder = st.empty()
    for i in range(len(string)):
        placeholder.markdown(string[:i] + "▌")
        time.sleep(interval)
    placeholder.markdown(string)
    st.session_state.messages.append({"role": "assistant", "content": string})


async def backend_is_healthy(client: LambdaClient) -> bool:
    return True


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    asyncio.run(main())
