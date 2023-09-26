#!/bin/bash

yum update -y
sudo yum install docker git
sudo service docker start

# fetch and install docker compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

cd /home/ec2-user
git clone https://github.com/TobiasWaslowski/lingolift.git && cd lingolift
docker-compose up -d --build
