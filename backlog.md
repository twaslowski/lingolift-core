# backlog

## Architectural

- ~~Move more exceptions to shared; as of now, a lot of exceptions are only declared in the backend,
  and parsed as ApplicationExceptions() in the shared client~~
- Actually, re-think Exception Handling entirely. There should be a less complicated way of solving it than I am doing
  now.
- Test Telegram Client. As the frontend and the telegram client converge, the tests on the telegram client
  will help develop confidence in the (largely untestable) frontend as well.
    - This actually works surprisingly well.
- Backend: Move it to Lambda? I considered this previously, but straight-up running the backend on lambda with a thin
  wrapper does not work, as the collective spaCy models end up using more memory than is allowed (150M). However,
  creating several small lambdas _would_ improve reliability and CI/CD options. I already invested a bunch of time
  making my Raspberry Pi reachable from the internet to host the flask server, but ultimately this scales way better. ✅
    - ~~I tried this; turns out it's a nightmare. There is a well-known issue where Pydantic has to be compiled for the
      correct platform;
      however, even with stuff like `pip install --platform manylinux2014_x86_64` I couldn't figure it out.
      Dockerizing would be another option, but that comes with more headaches plus having to handle Docker images in
      ECR. For now, I'll focus on~~
    - Dockerizing this is the way to go. The Pydantic issue turns out to be extremely hard to fix and to debug;
      I ended up building all the dependencies in a Docker container to emulate the x86_64 architecture that the
      lambda runtime uses, and at that point you might as well just use Docker. Managing ECR is a bit of a pain, but
      it's not too bad.
- Implement IAC. This will enable CI/CD usage, which I really need. DynDNS on my Raspberry Pi is turning out to be
  incredibly unreliable, so this is top priority. ✅
    - Create ECR ✅
    - Create Lambda ✅
- Implement CI/CD. ✅
    - Solve AWS Authentication from the pipeline ✅
    - Setup Github Actions ✅
- Figure out a smart way of arbitrarily creating Lambdas. Creating a Terraform module would be a good way to go;
however, coupling them together makes techdebt issue #1 more difficult to handle. ✅ 
- I need to figure out error handling in the lambdas. Using `context.fail()` or returníng bad Status Codes might
be good ways of achieving this.

## Tech Debt

- Lambdas require an ECR repository with Images in it. The creation order should be ECR -> Docker push to ECR -> Lambda.
  However, this is difficult to achieve as it requires to separate `terraform apply`s. This can be solved by manually
  pushing, but it creates an infrastructure state that I ideally would like to avoid.
- The current `backend/docker-util.sh` is pretty hacky. It does its job for now, but I would prefer having proper
  argument parsing and error handling.
- As I move towards a Lambda-oriented architecture, refactoring the backend would be a good idea. Specifically,
  splitting up the `service` package into different functionalities might make sense.
- The frontend is currently not particularly clean. For more complex features, we'll probably have to move to
  something more powerful anyhow, but keeping this clean for a while is probably important so we can add more features.
- Create a Trello board so I can get rid of this way of documenting progress.

## Features

- Translation stringification should not repeat the original sentence beyond a certain length
- Suggestions should only be rendered if the original sentence is a question ✅
    - ~~potentially, this could be solved via an LLM. At that point, a /meta endpoint might make sense. This endpoint
      could
      also handle the language identification parts of the application.~~
    - The above approach is profoundly overcomplicated. Checking
      if `'?' in translation.sentence or '?' in translation.translation` will likely cover 95% of usecases. If this is a
      priority, an approach of looking for interrogative words/phrases would probably be an easy way to achieve higher
      reliability.
- Explain morphological features more clearly. Requires work on the upos_explanation endpoint.
- Morphologizer. Hard to narrow down exactly in which ways this might work in an educationally valuable way, but spaCy
  allows for it – let's see if this is something that actually makes sense.

