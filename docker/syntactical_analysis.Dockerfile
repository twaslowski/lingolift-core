FROM public.ecr.aws/lambda/python:3.11.2024.02.07.18

RUN yum install -y git

ENV PYTHONPATH=/var/task/

# Set up a working directory
WORKDIR /var/task

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

CMD [ "nlp_lambda_handlers.syntactical_analysis_handler" ]
