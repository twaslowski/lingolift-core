import aiohttp

import requests

LINGOLIFT_BACKEND_ENDPOINT = "http://localhost:5001"


async def get_translation(sentence: str) -> dict:
    return requests.post(f"{LINGOLIFT_BACKEND_ENDPOINT}/translation", json={"sentence": sentence}).json()


async def get_suggestions(session: aiohttp.ClientSession, sentence: str) -> list[str]:
    async with session.post(f"{LINGOLIFT_BACKEND_ENDPOINT}/response-suggestion", json={"sentence": sentence}) as response:
        return await response.json()


async def get_literal_translation(session: aiohttp.ClientSession, sentence: str) -> list[dict]:
    async with session.post(f"{LINGOLIFT_BACKEND_ENDPOINT}/literal-translation",
                            json={"sentence": sentence}) as response:
        return await response.json()


async def get_syntactical_analysis(session: aiohttp.ClientSession, sentence: str, language: str) -> list[dict]:
    async with session.post(f"{LINGOLIFT_BACKEND_ENDPOINT}/syntactical-analysis",
                            json={"sentence": sentence, "language": language}) as response:
        return await response.json()


# To execute the get_all function and print results
if __name__ == "__main__":
    sentence_to_translate = "Хорошо, как твои дела?"
