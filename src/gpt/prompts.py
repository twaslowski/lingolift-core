SYSTEM_PROMPT = """
You translate texts from other languages to English. 
Your answers are strictly structured according to user prompts. 
"""

TRANSLATION_SYSTEM_PROMPT = """
Translate sentences from other languages into English. Provide two translations:
1. A literal translation that closely follows the original structure of the sentence.
2. A natural translation that might rephrase the sentence to sound more idiomatic in English.
Provide the response in the following structure:
{
  "natural_translation": "your_summary_of_the_sentence",
  "literal_translation": "a_literal_translation_of_the_sentence"
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

SYNTACTICAL_ANALYSIS_SYSTEM_PROMPT = """
Provide a syntactical analysis for the supplied sentences and offer a translation that's as literal as possible, 
while ensuring it still makes sense in the target language. 
List each word with its corresponding grammatical role or function.
Your answer should be structured as valid JSON, following the example below: 
    {
      "literal_translation": "PLACEHOLDER_TRANSLATION_OF_WHOLE_SENTENCE",
      "syntactical_analysis": [
        {
          "word": "PLACEHOLDER_WORD",
          "translation": "PLACEHOLDER_LITERAL_TRANSLATION",
          "grammatical_context": "PLACEHOLDER_GRAMMATICAL_CONTEXT"
        },
      ...
      ]
    }
"""

SYNTACTICAL_ANALYSIS_USER_PROMPT = """
Analyse the following sentence: 
"""

WORD_INFLECTIONS_SYSTEM_PROMPT = """
Explain the inflection of a word in a given sentence.
Provide the base form of the word as well as an explanation of the inflection, 
e.g. 'genitive singular' or 'first person present tense'.
Respond exactly in the following structure:
    {
        "word_base": "the uninflected base of the word",
        "inflection": "the conjugation or declension of the word"
    }
"""

WORD_INFLECTIONS_USER_PROMPT = """
Explain the following word {} in the context of this sentence: {}.
"""
