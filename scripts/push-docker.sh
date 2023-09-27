aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 246770851643.dkr.ecr.eu-central-1.amazonaws.com

docker tag lingolift-backend:latest 246770851643.dkr.ecr.eu-central-1.amazonaws.com/lingolift-backend:latest
docker push 246770851643.dkr.ecr.eu-central-1.amazonaws.com/lingolift-backend:latest

docker tag lingolift-frontend:latest 246770851643.dkr.ecr.eu-central-1.amazonaws.com/lingolift-frontend:latest
docker push 246770851643.dkr.ecr.eu-central-1.amazonaws.com/lingolift-frontend:latest
