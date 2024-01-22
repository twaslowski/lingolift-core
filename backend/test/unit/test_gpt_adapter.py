from llm import gpt_adapter


def test_parse_gpt_response():
    happy_path = """{
        "literal_translation": "Hello! How are you?",
        "words": [
            {
                "word": "Moin!",
                "translation": "Hello!"
            },
            {
                "word": "Wie",
                "translation": "How"
            },
            {
                "word": "geht",
                "translation": "goes"
            },
            {
                "word": "es",
                "translation": "it"
            },
            {
                "word": "dir",
                "translation": "you"
            }
        ]
    }"""
    result = gpt_adapter.parse_response(happy_path)
    assert isinstance(result, dict)


def test_parser_manages_trailing_commas():
    happy_path = """{
        "literal_translation": "Hello! How are you?",
        "words": [
            {
                "word": "Moin!",
                "translation": "Hello!",
            },
            {
                "word": "Wie",
                "translation": "How",
            },
            {
                "word": "geht",
                "translation": "goes",
            },
            {
                "word": "es",
                "translation": "it",
            },
            {
                "word": "dir",
                "translation": "you",
            }
        ]
    }"""
    result = gpt_adapter.parse_response(happy_path)
    assert isinstance(result, dict)
