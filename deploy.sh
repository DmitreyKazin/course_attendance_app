#!/usr/bin/bash

echo "DEPLOY TO PRODUCTION: STARTED"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yaml ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com:/home/ec2-user/

# login with ssh to ec2-user on production server & rm images and containers
ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"docker ps -aq | xargs docker rm -f"

ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"docker images -q | xargs docker rmi -f"

# login with ssh to ec2-user on production server & bring the application up
ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"cd /home/ec2-user"

ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"docker-compose -f docker-compose-prod.yaml up -d --build"

echo "DEPLOY TO PRODCUTION: SUCCESS"


