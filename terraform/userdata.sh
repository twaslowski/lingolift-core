#!/bin/bash

yum update -y
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git -y

# install python
wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz
tar xzf Python-3.11.4.tgz
cd Python-3.11.4
./configure
make altinstall

cd /home/ec2-user
git clone https://github.com/TobiasWaslowski/lingolift.git && cd lingolift

./scripts/run.sh
