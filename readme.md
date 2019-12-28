jsnarvasa.com
=============
Author: Jesse S. Narvasa
Date: 14 October 2019

***

## Setup
1. Create virtualenv
2. Copy .service file to /etc/systemd/system/ - this allows you to do systemctl calls
3. Create nginx entry in sites-available directory - this creates the nginx entry for nginx to link to uwsgi
4. Create link file of nginx entry in sites-enabled directory
5. Run "sudo systemctl start jsnarvasa.service"
6. May need to restart nginx "sudo systemctl restart nginx" or just reload

#### Inserting Area Boundary static data in MySQL database
1. Update geo-countries_zip geojson file to be a .py file and create a dictionary variable that countains the whole file
2. run geojson_sql_constructor.  This will create a boundaries.sql file
3. Run mysql -f -uroot -p'<password>' CornAndCheese < boundaries.sql to upload boundaries data, while forcing write since some entries may violate unique constraints

***

## Licenses
geoJSON boundary data used within the visual scratch map component of PhotoBlog has been acquired through the sources below, where the original data is public domain.

[Natural Earth][naturalearth]
[Lexman][lexman]
[Open Knowledge Foundation][okfn]

[naturalearth]: http://www.naturalearthdata.com/
[lexman]: http://github.com/lexman
[okfn]: http://okfn.org/

***

## Legacy
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