#!/bin/sh

# Script used to automatically create MySQL Docker container and mount data directory to home directory
docker run --name=cornandcheesedb \
--mount type=bind,src=/home/narvjes/repository/cornandcheese/database/data,dst=/var/lib/mysql \
-d mysql/mysql-server