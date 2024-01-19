FROM amazonlinux:2023

# Install Python and zip
RUN yum install -y git zip python3-pip

# Set up a working directory
WORKDIR /var/task

# Copy the requirements.txt file into the container
COPY package/requirements.txt .

COPY lambda_function.py .

# Install the Python dependencies and package them in a zip file
RUN python3 -m pip install -r requirements.txt -t /var/task/python/lib/python3.9/site-packages/

# Create a zip file with the correct directory structure
RUN zip -r /var/task/dependencies.zip .
