#!/bin/bash
 
echo 'Starting to Deploy...'
ssh ec2-user@ec2-18-163-195-22.ap-east-1.compute.amazonaws.com " sudo docker image prune -f 
        cd COMP_GIT 
        sudo docker-compose down
        git fetch origin
        git reset --hard origin/develop  &&  echo 'You are doing well'
        cd Docker
        sudo docker-compose -f docker-compose.yaml up -d
        "
echo 'Deployment completed successfully'
