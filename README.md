# CAtS 

## How to access different services ?

##### CAtS Web-service

```
${IPv4_Public_IP}:8000
```

##### Jenkins

```
${IPv4_Public_IP}:8080
```

##### SonarQube

```
${IPv4_Public_IP}:9000
```



## How to access PostgreS on AWS ?

##### Log into AWS server via SSH:

```
ssh -i CAtS.pem ubuntu@${IPv4_Public_IP}
```

##### To login PostgreS on AWS:

```
psql -h localhost -p 5432 -U cats cats
```



## How to migrate the database ?

##### Delete current migrations folder under `./CAS_WEB/cas`

```
rm -rf migrations
```

##### Make migration for CAtS app in `./CAS_WEB`

```
python3 manage.py makemigrations ${app_name}
```

###### Eg: 

```
python3 manage.py makemigrations cas
```

##### Show all the SQL instructions for migrate operation 

```
python3 manage.py sqlmigrate ${app_name} ${version_name}
```

###### Eg: 

```
python3 manage.py sqlmigrate cas 0001_initial
```

##### After changing functions in `./CAS_WEB/cas/models.py`, redo make migration

```
python3 manage.py makemigrations ${app_name}
```

##### Then you can see the newest version of migration under `./CAS_WEB/cas/migrations`, then you can migrate the database

```
python3 manage.py migrate ${app_name}
```



## How to start the service on virtual machine ?

##### Run vagrant on local machine under root folder

```
vagrant up
```

##### Connect to the shared folder on virtual machine

```
vagrant ssh
cd /vagrant/
```

##### Config the `./CAS_WEB/webapps/settings.py` with current IP address,

##### And start the server with localhost 

```
python3 manage.py runserver 0.0.0.0:8000
```

##### Connect to the server via internet browser

```
192.168.56.22:8000
```

## How to build docker image ? 

##### Note: Please install `docker` and `docker-compose` before you build the docker image

##### To build and run the image

```
docker-compose up
```

##### To run in daemon

```
docker-compose up -d
```

















