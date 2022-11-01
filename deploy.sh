#!/usr/bin/bash

echo "DEPLOY TO PRODUCTION: STARTED"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yaml \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com:/home/ec2-user/

# copying mysql-env
scp -i "id_rsa" -r /home/ec2-user/workspace/release-pipeline/env/ \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com:/home/ec2-user/

# login with ssh to ec2-user on production server & cd ~
ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"cd /home/ec2-user"

# login with ssh to ec2-user on production server & bring app down
ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"docker-compose -f docker-compose-prod.yaml down"

ssh -i "id_rsa" \
ec2-user@ec2-35-78-75-153.ap-northeast-1.compute.amazonaws.com \
-o BatchMode=yes -o StrictHostKeyChecking=no \
"docker-compose -f docker-compose-prod.yaml up -d --build"

echo "DEPLOY TO PRODCUTION: SUCCESS"


