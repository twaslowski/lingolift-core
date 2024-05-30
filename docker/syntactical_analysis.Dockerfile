FROM public.ecr.aws/lambda/python:3.11.2024.02.07.18

RUN yum install -y git

# Set up a working directory
WORKDIR /lingolift

# Copy project
COPY lingolift/generative ./generative/
COPY lingolift/llm ./llm/
COPY lingolift/util ./util/
COPY lingolift/nlp ./nlp/

COPY lingolift/nlp_lambda_handlers.py .
COPY lingolift/abstract_context_container.py .
COPY lingolift/nlp_lambda_context_container.py .

# Install dependencies
COPY package/requirements.txt ./
RUN python3 -m pip install -r requirements.txt

CMD [ "nlp_lambda_handlers.syntactical_analysis_handler" ]
