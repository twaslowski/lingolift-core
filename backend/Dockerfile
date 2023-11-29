FROM python:3.11

ARG OPENAI_API_KEY

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . backend/
ENV PYTHONPATH=app
ENV FLASK_APP=backend/app

CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001" ]