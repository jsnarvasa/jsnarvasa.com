#!/bin/bash

# Script to login to MySQL command line
pw="$(docker logs cornandcheesedb 2>&1 | grep GENERATED)"
echo ${pw:38:28}
docker exec -it cornandcheesedb mysql -uroot -p