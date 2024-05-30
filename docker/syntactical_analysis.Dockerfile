FROM public.ecr.aws/lambda/python:3.11.2024.02.07.18

RUN yum install -y git

# Set up a working directory
WORKDIR /lingolift

# Copy project
COPY lingolift ./

# Install dependencies
COPY package/requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "lingolift.nlp_lambda_handlers.syntactical_analysis_handler" ]
