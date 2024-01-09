from backend.llm.message import Message, SYSTEM, USER
from gpt_adapter import openai_exchange

SYSTEM_PROMPT = """Identify whether a customer has supplied a customer number or not. 
Respond with a JSON of the following structure:
{
    "customer_number": 1234556
}
The "customer_number" field should be null if not provided in the message.
"""

customer_message = "i found it! my customer number is 2394238424"

print(openai_exchange(messages=[Message(SYSTEM, SYSTEM_PROMPT), Message(USER, customer_message)]))

