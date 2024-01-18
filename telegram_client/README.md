# telegram_client

This is the Telegram client for the GrammR application. It behaves the same way the frontend does, using a lot
of the shared code.

## Running the application

Create a `.env` file containing the `TELEGRAM_TOKEN` as well as the connection configuration:

```
TELEGRAM_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ
BACKEND_PROTOCOL=http
BACKEND_HOST=localhost
BACKEND_PORT=5001
```

If you're just running everything locally, you can omit the connection configuration, as those are the exact
default values for the shared.Client() anyway.