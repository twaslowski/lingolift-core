# backlog



## Architectural

- Unify telegram_client and frontend functions, such as the find_analysis() and coalesce_analysis() functions
- Move more exceptions to shared; as of now, a lot of exceptions are only declared in the backend,
and parsed as ApplicationExceptions() in the shared client
- Test Telegram Client. As the frontend and the telegram client converge, the tests on the telegram client
will help develop confidence in the (largely untestable) frontend as well.

## Features

- Explain morphological features more clearly. Requires work on the upos_explanation endpoint.