def mock_response() -> dict:
    return {
        "literal_translation": "How are things with you today?",
        "response_suggestions": [
            {
                "response": "У меня все хорошо.",
                "translation": "I'm doing well."
            },
            {
                "response": "Не очень.",
                "translation": "Not so good."
            }
        ],
        "sentence_breakdown": [
            {
                "grammatical_context": "interrogative pronoun",
                "translation": "How",
                "word": "Как"
            },
            {
                "grammatical_context": "preposition",
                "translation": "with",
                "word": "у"
            },
            {
                "grammatical_context": "personal pronoun (genitive case)",
                "translation": "you",
                "word": "тебя"
            },
            {
                "grammatical_context": "adverb",
                "translation": "today",
                "word": "сегодня"
            },
            {
                "grammatical_context": "noun",
                "translation": "things",
                "word": "дела"
            }
        ],
        "summary": "How are you doing today?"
    }
