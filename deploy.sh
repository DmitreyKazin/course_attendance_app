#!/usr/bin/bash

echo "DEPLOY TO PRODUCTION: STARTED"

# ssh login to ec2-user in production server
cd /home/ec2-user/.ssh

ssh -i "app-production.pem" ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com

# deleting existing containers & images
docker ps -aq | xargs docker rm -f
docker images -q | xargs docker rmi -f



