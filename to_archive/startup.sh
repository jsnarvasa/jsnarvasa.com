#!/bin/bash

# Script used to automatically create MySQL Docker container and mount data directory to home directory
docker run --name=cornandcheesedb \
--mount type=bind,src=/home/narvjes/cornandcheese/database/data,dst=/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=password \
-d mysql:5.7.22