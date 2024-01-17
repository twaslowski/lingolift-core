# backlog



## Architectural

- Move more exceptions to shared; as of now, a lot of exceptions are only declared in the backend,
and parsed as ApplicationExceptions() in the shared client
- Test Telegram Client. As the frontend and the telegram client converge, the tests on the telegram client
will help develop confidence in the (largely untestable) frontend as well.

## Features

- Translation stringification should not repeat the original sentence beyond a certain length
- Suggestions should only be rendered if the original sentence is a question
  - potentially, this could be solved via an LLM. At that point, a /meta endpoint might make sense. This endpoint could
  also handle the language identification parts of the application.
- Explain morphological features more clearly. Requires work on the upos_explanation endpoint.