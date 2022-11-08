#!/usr/bin/bash

# defining environment to deploy
STAGE=${1}
PROD=172.31.7.202
STAGING=172.31.47.116
DEPLOY_ENV=''

if [[ ${STAGE}=="production" ]]
then
	DEPLOY_ENV=${PROD}
else
	DEPLOY_ENV=${STAGING}
fi

echo "DEPLOY TO ${STAGE} ENVIRONMENT: START"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yml \
ec2-user@${DEPLOY_ENV}:/home/ec2-user/

# copying mysql-env to production server
scp -i "id_rsa" -r /home/ec2-user/workspace/release-pipeline/env/ \
ec2-user@${DEPLOY_ENV}:/home/ec2-user/

# login with ssh to ec2-user & bring the application up
ssh -i "id_rsa" \
ec2-user@${DEPLOY_ENV} \
-o BatchMode=yes -o StrictHostKeyChecking=no \
<< EOF
cd /home/ec2-user/
docker-compose -f docker-compose-prod.yml down
docker images -q | xargs docker rmi -f
docker-compose -f docker-compose-prod.yml up -d --build
EOF

echo "DEPLOY TO ${STAGE} ENVIRONMENT: SUCCESS"
