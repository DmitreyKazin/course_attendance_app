#!/usr/bin/bash

echo "DEPLOY TO PRODUCTION: START"

# copying docker-compose-prod.yaml to production server
cd /home/ec2-user/.ssh
scp -i "id_rsa" /home/ec2-user/workspace/release-pipeline/docker-compose-prod.yaml \
ec2-user@172.31.7.202:/home/ec2-user/

# copying mysql-env to production server
scp -i "id_rsa" -r /home/ec2-user/workspace/release-pipeline/env/ \
ec2-user@172.31.7.202:/home/ec2-user/

# login with ssh to ec2-user on production server & bring the application up
ssh -i "id_rsa" \
ec2-user@172.31.7.202 \
-o BatchMode=yes -o StrictHostKeyChecking=no \
<< EOF
	cd /home/ec2-user/
	docker-compose -f docker-compose-prod.yaml down
	docker-compose -f docker-compose-prod.yaml up -d --build
EOF

echo "DEPLOY TO PRODCUTION: SUCCESS"


