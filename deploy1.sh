#!/usr/bin/env bash

# defining environment to deploy
STAGE=${1}
PROD_IP="172.31.7.202"
STAGING_IP="172.31.57.116"
DEPLOY_ENV=""

if [ ${STAGE}=="production" ];
then
	DEPLOY_ENV=${PROD_IP}
elif [ ${STAGE}=="staging" ];
then
	DPELOY_ENV=${STAGING_IP}
else
	echo "ERROR!!!\nONLY 'production' OR 'test' ARE ACCEPTED"
	exit 1

