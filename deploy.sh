#!/usr/bin/bash

# defining environment to deploy
STAGE=$1
PROD_IP="172.31.7.202"
STAGING_IP="172.31.57.116"
DEPLOY_ENV=""

if [ $STAGE=="production" ];
then
	DEPLOY_ENV=$PROD_IP
elif [ $STAGE=="staging" ];
then
	DPELOY_ENV=$STAGING_IP
else
	echo "ERROR!!!\nONLY 'production' OR 'test' ARE ACCEPTED"
	exit 1

echo "DEPLOY TO ${STAGE} ENVIRONMENT: START"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yaml \
ec2-user@${DEPLOY_ENV}:/home/ec2-user/

# copying mysql-env to production server
scp -i "id_rsa" -r /home/ec2-user/workspace/release-pipeline/env/ \
ec2-user@${DEPLOY_ENV}:/home/ec2-user/

# login with ssh to ec2-user on production server & bring the application up
ssh -i "id_rsa" \
ec2-user@${DEPLOY_ENV} \
-o BatchMode=yes -o StrictHostKeyChecking=no \
<< EOF
		cd /home/ec2-user/
		docker-compose -f docker-compose-prod.yaml down
		docker images -q | xargs docker rmi -f
		docker-compose -f docker-compose-prod.yaml up -d --build
EOF

echo "DEPLOY TO ${STAGE} ENVIRONMENT: SUCCESS"
