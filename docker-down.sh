#!/bin/bash

docker-compose down
docker volume rm $(docker volume ls -q)
docker rmi $(docker images -qa -f 'dangling=true')