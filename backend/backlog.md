# backlog



## Architectural

- ~~Move more exceptions to shared; as of now, a lot of exceptions are only declared in the backend,
and parsed as ApplicationExceptions() in the shared client~~
- Actually, re-think Exception Handling entirely. There should be a less complicated way of solving it than I am doing now.
- Test Telegram Client. As the frontend and the telegram client converge, the tests on the telegram client
will help develop confidence in the (largely untestable) frontend as well.
  - This actually works surprisingly well.
- Frontend: Make it clean. For more complex features, we'll probably have to move to something more powerful anyhow, but keeping this clean for a while is probably important so we can add more features.

## Features

- Translation stringification should not repeat the original sentence beyond a certain length
- Suggestions should only be rendered if the original sentence is a question ☑️
  - ~~potentially, this could be solved via an LLM. At that point, a /meta endpoint might make sense. This endpoint could
  also handle the language identification parts of the application.~~
  - The above approach is profoundly overcomplicated. Checking if `'?' in translation.sentence or '?' in translation.translation` will likely cover 95% of usecases. If this is a priority, an approach of looking for interrogative words/phrases would probably be an easy way to achieve higher reliability.
- Explain morphological features more clearly. Requires work on the upos_explanation endpoint.
