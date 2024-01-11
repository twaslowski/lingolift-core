# lingolift

This is an application to enhance the process of learning a language when chatting with native speakers.
Specifically, this application's value is this:

- It provides translations for arbitrary sentences
- It provides literal translations for each word in a given sentence, enhancing language comprehension
- It provides response suggestions
- It provides a syntactical analysis, using the spaCy NLP Library

## Overview

This codebase is roughly segmented into three parts: A **backend**, a **frontend** and a **Telegram** _bot_.
Essentially, the backend runs as a Flask server (that can be dockerized), which provides the relevant functionality
via four different endpoints:

`POST /translate`

`POST /responses`

`POST /literal-translation`

`POST /syntactical-analysis`

The Telegram Bot and the Frontend can both be run as clients for this server to render the
translation info to end-users. The backend utilizes the OpenAI API to generate the relevant information.
You can run the backend with `make backend` and then either – or both – client applications with
`make frontend` and `make bot`, respectively.

## Running

You can run this application yourself. You will need an OpenAI API key and, if you choose
to run the Telegram Bot, a Telegram Bot token. Generate them and

`echo "OPENAI_API_KEY=sk-abcdef0123456789" > backend/.env`

`echo "TELEGRAM_TOKEN=012345789:abcdefghijklmnop" > telegram_client/.env`

After that, simply run `make backend` and `make bot` to start the applications.

The frontend is, as of now, not being used or maintained. I'm not good at building frontends
and I don't particularly enjoy it. I hadn't touched the frontend code for a few months, but it suddenly
stopped working and I couldn't be bothered to do the maintenance. Getting this done (or probably re-writing
the frontend from scratch) seems like an interesting future endeavor.

## Todos

If you feel like this project is interesting, I'm happy about contributions. There are several things
I would like to do:

- The grammatical analysis with spaCy needs to get better. As of now, it is not particularly understandable,
since I simply return the morphology features as a string. Additional work could be done here to make this
more user-friendly.
- The analysis could be expanded in several ways:

## Further Reading

https://universaldependencies.org/format.html#morphological-annotation

https://universaldependencies.org/u/feat/Degree.html

https://spacy.io/api/morphology#morphanalysis

https://www.nltk.org/

## The Role of LLMs

It should be noted that this application is more than just a simple GPT-wrapper.