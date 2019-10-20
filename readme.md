jsnarvasa.com
=============
Author: Jesse S. Narvasa
Date: 14 October 2019

#### Server Setup
***
1. Login as root
2. Create new user
3. Assign new user sudo group
4. Copy SSH key to new user to allow SSH without root
	rsync --archive --chown=narvjes:narvjes ~/.ssh /home/narvjes
5. Turn off SSH for root
	vi sshd_config
	Set PermitRootLogin no and save
	Restart ssh service by sudo systemctl reload sshd
6. Add user to docker group
	sudo usermod -aG docker ${USER}


#### Docker Initialisations
***
Handy for scripts:
sed -i -e 's/\r$//' scriptname.sh

Things to Note:
* app docker container name is cornandcheese and the image is tagged as cornandcheese
* MySQL docker container name is cornandcheesedb
* connection string in YAML should be to MySQL docker container i.e. cornandcheesedb
* MySQL docker database name is only cornandcheese

1. Initialise database
docker run --name=cornandcheesedb \
--mount type=bind,src=/home/narvjes/cornandcheese/database/data,dst=/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=password \
-d mysql:5.7.22

2. Create database, MySQL will not accept connections until db is created
docker exec -it cornandcheesedb mysql -uroot -p
CREATE DATABASE cornandcheese
USE cornandcheese

3. Initialise web app
git pull origin master
update database_config.yaml mysql_host value to 'cornandcheesedb'
docker build -t cornandcheese .
docker run --name cornandcheese --link cornandcheesedb:mysql -d -p 80:80 -t cornandcheese