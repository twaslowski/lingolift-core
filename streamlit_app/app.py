import time
from typing import Optional

import requests
import streamlit as st

TITLE = "lingolift"


def main():
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
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            render_message("Translating ...", 0.05)
            sentence = st.session_state.messages[0].get('content')
            translation = fetch_translation(sentence)

            # fetch remaining data
            suggestions = fetch_suggestions(sentence)
            literal_translations = fetch_literal_translations(sentence)
            syntactical_analysis = fetch_syntactical_analysis(sentence, "ru")
            analysis_rendered = coalesce_analyses(literal_translations, syntactical_analysis)
            render_message(translation, 0.025)
            render_message(suggestions, 0.025)
            render_message(analysis_rendered, 0.025)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": translation})


def fetch_translation(sentence: str) -> str:
    print(f"fetching translation for sentence '{sentence}'")
    response = requests.post("http://localhost:5001/translation", json={"sentence": sentence}).json()
    print(f"received translation for sentence '{sentence}': '{response}'")
    return f"""**Translation**

'*{sentence}*' is {response['language']} and translates to '*{response['translation']}*'"""


def fetch_suggestions(sentence: str) -> str:
    response = requests.post("http://localhost:5001/response-suggestion", json={"sentence": sentence}).json()
    print(f"Received suggestions for sentence '{sentence}': '{response}'")
    response_string = "**Response suggestions:**\n\n"
    for suggestion in response['response_suggestions']:
        response_string += f"*'{suggestion['suggestion']}'*\n\n"
        response_string += f"{suggestion['translation']}\n\n"
    return response_string


def fetch_literal_translations(sentence: str) -> Optional[dict]:
    response = requests.post("http://localhost:5001/literal-translation", json={"sentence": sentence}).json()
    print(f"Received literal translations for sentence '{sentence}': '{response}'")
    return response


def fetch_syntactical_analysis(sentence: str, language: str) -> Optional[dict]:
    response = requests.post("http://localhost:5001/syntactical-analysis",
                             json={"sentence": sentence,
                                   "language": language}).json()
    print(f"Received syntactical analysis for sentence '{sentence}': '{response}'")
    return response


def coalesce_analyses(literal_translations: dict, syntactical_analysis: dict) -> str:
    """
    If both a literal translation of the words in the sentence and the syntactical analysis (i.e. part-of-speech
    tagging) are available, they get coalesced in this function, meaning each word gets displayed alongside its
    translation and its morphological features. If only the literal translation is available, the translations
    are displayed. If neither or only the morphological analysis is available, the function returns an error message.
    :param literal_translations:
    :param syntactical_analysis:
    :return:
    """
    if error := literal_translations.get('error'):
        return f"The analysis failed: {error}"
    response_string = "**Vocabulary and Grammar breakdown**\n\n"
    if error := syntactical_analysis.get('error'):
        response_string += f"Morphological analysis failed: {error}; however, the literal translation is available.\n\n"
    for word in literal_translations['literal_translations']:
        word_analysis = find_analysis(word['word'], syntactical_analysis.get('syntactical_analysis'))
        response_string += f"*{word['word']}*: {word['translation']}"
        if word_analysis:
            response_string += f" (lemma: {word_analysis['lemma']}, " \
                               f"morphology {word_analysis['morphology']}, " \
                               f"dependencies: {word_analysis['dependencies']})\n\n"
        else:
            response_string += "\n\n"
    return response_string


def find_analysis(word: str, syntactical_analysis: dict) -> dict:
    if syntactical_analysis is None:
        return {}
    for entry in syntactical_analysis:
        if entry['word'] == word and entry['morphology'] != '':
            return entry
    return {}


def render_message(string: str, interval: float):
    placeholder = st.empty()
    for i in range(len(string)):
        placeholder.markdown(string[:i] + "▌")
        time.sleep(interval)
    placeholder.markdown(string)


if __name__ == '__main__':
    main()
