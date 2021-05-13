# PA036_ProjectDB
Repository to PA036 project DB  
https://github.com/xtuzil/PA036_ProjectDB

#### Team members:
Katarina Hermanova,
Marian Koncek,
Matej Tuzil,
Vojtech Spevak


In Fedora 33 please run this project in /tmp/ file to avoid "Permission denied" type of errors (sorry for inconveniences)
In Windows run this project from Public folder or set the permissions as described in Data preparation section

## Requirements
* Python 3
* PostgreSQL
* MongoDB
* Psycopg2
* PyMongo
* PyYAML
* Matplotlib


## Instalation

### Postgres

MacOS:

    brew install postgresql

Fedora 33 + DB setup (can skip Creating Postgres db below):

    sudo dnf update -y
    sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-33-x86_64/pgdg-fedora-repo-latest.noarch.rpm`
    sudo dnf install -y postgresql13-server
    sudo /usr/pgsql-13/bin/postgresql-13-setup initdb
    sudo systemctl enable postgresql-13
    sudo systemctl start postgresql-13
    sudo systemctl status postgresql-13
    sudo su - postgres
    psql
    alter user postgres with password 'admin@123';
    CREATE USER admin WITH SUPERUSER PASSWORD 'admin';
    create database pa036;
    exit
    logout

Windows - Download the installer from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads and follow the installation.

### MongoDB
#### MacOS

    brew install mongodb-community@4.4

#### Fedora 33:

    sudo dnf install nano
    sudo nano /etc/yum.repos.d/mongodb.repo`

add the following text:

    [mongodb-org-4.4]
    name=MongoDB Repository
    baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/4.4/x86_64/
    gpgcheck=1
    enabled=1
    gpgkey=https://www.mongodb.org/static/pgp/server-4.4.asc

Install mongo:

    sudo dnf install mongodb-org
    sudo systemctl daemon-reload
    sudo systemctl start mongod
    sudo systemctl status mongod
    mongod -version

#### Windows
Follow the steps described in https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
including setting up the MongoDB as a Windows service.

### Psycopg2

    pip install psycopg2

Fedora 33:

    sudo yum install libpq-devel python-devel
    pip install psycopg2 # (if run with error continue below)
    pip install psycopg2-binary
    pip freeze | grep psycopg2

### PyMongo

    python -m pip install pymongo

### PyYAML

    pip install PyYAML

### jsonlines

    pip install jsonlines

### matplotlib

    pip install matplotlib

in Fedora 33:

    sudo dnf install python3-matplotlib.x86_64

## Creating Postgres db

    initdb /usr/local/var/postgres
    pg_ctl -D /usr/local/var/postgres start
    createdb pa036
    psql pa036
    CREATE USER admin WITH SUPERUSER PASSWORD 'admin'; -- (to psql)
    exit

## Data preparation
You must provide file personData.json in Data directory. If the file is zipped, unzip it with:

    gunzip -k personData.json.gz

Windows - set the access permissions of person.json: `Properties -> Security -> Edit -> Add -> "yourcomputername\Users"`

## Running the application
After having set up the database daemons (see how it is done in `entrypoint.sh` execute `python3 main.py`.
The program writes results to a file `results.json`. If such file already exists, the results are appended.

Graphs can be created after having the results by running `python3 visualization.py`.
It created a larger number of pictures + 2 aggregate pictures (`queries.png` and `queries-grouped.png`)

There is a `Dockerfile` which can be used to execute the whole process with just 3 commands.
It is described in the file.

Of course for that you would need `docker` or `podman`.


## Application hierarchy

.  <br />
|_ __Data__  <br />
|______ __.DS_Store__     <br />
|______ __DataGenerator.py__    <br />
|______ __SpeedViolationDataGenerator.py__ _(responsible for creating SpeedViolationData)_<br />
|______ __json-generator_schema.txt__    <br />
|______ __personData.json.gz__ _(personData to unzip)_   <br />
|_ __results__ _(contains directories with results from different machines)_   <br />
|______ __mkoncek__ _(Fedora 34 inside container on Fedora 33 Lenovo ThinkPad T480s)_   <br />
|______ __mtuzil__ _(macOS Big Sur Version 11.2.3 on MacBook Pro 2017)_   <br />
|______ __khermano__ _(Fedora 33 running on Lenovo ThinkPad T590)_    <br />
|______ __vspevak__ _(Windows 10 Home running on Acer Swift SF314-52G)_     <br />
|_ __.gitignore__ <br />
|_ __Dockerfile__ <br />
|_ __ExperimentApp.py__ _(runs experiment from both DBs)_ <br />
|_ __LICENSE__ <br />
|_ __MongoDB.py__ _(takes care about MongoDB e.g. data loading, indexes...)_ <br />
|_ __Postgres.py__ _(takes care about PostgreSQL DB e.g. data loading, indexes...)_ <br />
|_ __README.md__ <br />
|_ __entrypoint.sh__ <br />
|_ __main.py__ <br />
|_ __queries.yaml__ _(MongoDB and Postgres experiments)_ <br />
|_ __visualization.py__ _(for creating graphs of results)_ <br />