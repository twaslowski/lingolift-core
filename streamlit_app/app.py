import time

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
            translation = fetch_translation(st.session_state.messages[0].get('content'))

            # fetch remaining data
            suggestions = fetch_suggestions(st.session_state.messages[0].get('content'))
            render_message(translation, 0.025)
            render_message(suggestions, 0.025)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": translation})


def fetch_translation(sentence: str) -> str:
    response = requests.post("http://localhost:5001/translate", json={"sentence": sentence}).json()
    print(f"received translation for sentence '{sentence}': '{response}'")
    return f"""**Translation**

'*{sentence}*' is {response['language']} and translates to '*{response['translation']}*'"""


def fetch_suggestions(sentence: str) -> str:
    response = requests.post("http://localhost:5001/responses", json={"sentence": sentence}).json()
    print(f"Received suggestions for sentence '{sentence}': '{response}'")
    response_string = "**Response suggestions:**\n\n"
    for suggestion in response['response_suggestions']:
        response_string += f"*'{suggestion['suggestion']}'*\n\n"
        response_string += f"{suggestion['translation']}\n\n"
    return response_string


def render_message(string: str, interval: float):
    placeholder = st.empty()
    for i in range(len(string)):
        placeholder.markdown(string[:i] + "▌")
        time.sleep(interval)
    placeholder.markdown(string)


if __name__ == '__main__':
    main()
