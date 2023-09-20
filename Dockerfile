FROM python:3.11

ARG MOCK
ARG OPENAI_API_KEY

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]