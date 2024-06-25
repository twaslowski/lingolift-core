FROM public.ecr.aws/lambda/python:3.12.2024.06.19.12

RUN yum install -y git

ENV PYTHONPATH=/var/task/

# Set up a working directory
WORKDIR /var/task

# And corresponding spacy model id, e.g. "en_core_web_sm"
ARG SPACY_MODEL
ENV SPACY_MODEL=${SPACY_MODEL}

# Copy project
COPY lingolift/generative ./lingolift/generative/
COPY lingolift/llm ./lingolift/llm/
COPY lingolift/util ./lingolift/util/
COPY lingolift/nlp ./lingolift/nlp/

COPY lingolift/nlp_lambda_handlers.py ./nlp_lambda_handlers.py
COPY lingolift/abstract_context_container.py ./lingolift/abstract_context_container.py
COPY lingolift/nlp_lambda_context_container.py ./lingolift/nlp_lambda_context_container.py

# Install dependencies
COPY package/requirements.txt ./
RUN python3 -m pip install -r requirements.txt

# Install spaCy model
RUN python3 -m spacy download ${SPACY_MODEL}

CMD [ "nlp_lambda_handlers.syntactical_analysis_handler" ]
