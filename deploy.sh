#!/usr/bin/bash

echo "DEPLOY TO PRODUCTION: STARTED"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yaml ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com:/home/ec2-user/

# login with ssh to ec2-user on production server
#ssh -i "app-production.pem" ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com

# delete existing containers & images
#docker ps -aq | xargs docker rm -f
#docker images -q | xargs docker rmi -f

# bring the application up
#cd /home/ec2-user
#docker-compose -f docker-compose-prod.yaml -d --build

#echo "DEPLOY TO PRODCUTION: SUCCESS"


