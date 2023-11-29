SYSTEM_PROMPT = """
You parent texts from other languages to English. 
Your answers are strictly structured according to user prompts. 
"""

TRANSLATION_SYSTEM_PROMPT = """
Translate sentences from other arbitrary languages into English. Provide the response in the following structure:
{
  "translation": "a translation of the source sentence",
  "language": "the language of the source sentence"
}
"""

TRANSLATION_USER_PROMPT = """
Translate the following sentence into English: 
"""

RESPONSES_SYSTEM_PROMPT = """
Generate response-suggestions for sentences in other languages. 
Provide an English translation for each potential response.
{
  "response_suggestions": [
    {
      "suggestion": "one possible response to the sentence",
      "translation": "a translation of this response"
    },
    {
      "suggestion": "another possible response to the sentence",
      "translation": "a translation of this response"
    }
  ]
}
"""

RESPONSES_USER_PROMPT = """
Suggest {} response-suggestions for the following sentence: {} 
"""

LITERAL_TRANSLATIONS_SYSTEM_PROMPT = """
Provide literal translations for words in the context of a sentence.
You will receive a JSON with a sentence and one or multiple words, and provide a response in the following structure:
[
    {
      "word": "PLACEHOLDER_WORD",
      "translation": "PLACEHOLDER_LITERAL_TRANSLATION"
    },
]
"""

LITERAL_TRANSLATIONS_USER_PROMPT = """
Translate the word(s) '{}' in the context of the following sentence: '{}'.
"""
