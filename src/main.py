import logging
import os

import openai
from dotenv import load_dotenv

from gpt_adapter import chat_completion
from message import Message, SYSTEM
from prompts import SYSTEM_PROMPT

# setup
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename="log")

if __name__ == '__main__':
    session = [Message(role=SYSTEM, content=SYSTEM_PROMPT)]
    response = chat_completion(session, "Кого потеряла Россия в нем?")
    print(response)
