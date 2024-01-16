TRANSLATION_SYSTEM_PROMPT = """
Translate sentences from other arbitrary languages into English and identify the source language.
The source language should be returned as a ISO-3166 alpha-2 code.
Provide the response in the following JSON structure. For example:
{
  "translation": "Where is the Library?",
  "language": "ES"
}
"""

TRANSLATION_USER_PROMPT = """
Translate the following sentence into English: 
"""

RESPONSES_SYSTEM_PROMPT = """
Generate response-suggestions for sentences in other languages. 
Provide an English translation for each potential response in the following JSON structure:
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
[{
      "word": "PLACEHOLDER_WORD",
      "translation": "PLACEHOLDER_LITERAL_TRANSLATION"
}]
"""

LITERAL_TRANSLATIONS_USER_PROMPT = """
Translate the word(s) '{}' in the context of the following sentence: '{}'.
"""
