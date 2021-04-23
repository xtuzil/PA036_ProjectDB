FROM fedora:34

# Mongo repository
RUN echo $'[mongodb-upstream]\n\
name=MongoDB Upstream Repository\n\
baseurl=https://repo.mongodb.org/yum/redhat/8Server/mongodb-org/4.2/x86_64/\n\
gpgcheck=1\n\
enabled=1\n\
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc' \
> /etc/yum.repos.d/mongodb.repo

RUN dnf -y install postgresql postgresql-server python3-psycopg2 mongodb-org python3-pymongo python3-pip

RUN pip3 install pyaml

# Initialize PostgreSQL database with initial tables and users
RUN \
su - postgres -c "/usr/bin/initdb" && \
su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start" && \
su - postgres -c "createdb pa036" && \
su - postgres -c "createuser admin" && \
su - postgres -c "/usr/bin/pg_ctl stop" && \
:

# Intialize a place for MongoDB to store data
RUN mkdir -p /var/lib/mongo/data

COPY "Data/" "/root/pa036/Data/"
COPY "entrypoint.sh" "/root/pa036/"
COPY "ExperimentApp.py" "/root/pa036/"
COPY "main.py" "/root/pa036/"
COPY "MongoDB.py" "/root/pa036/"
COPY "Postgres.py" "/root/pa036/"
COPY "queries.yaml" "/root/pa036/"

WORKDIR "/root/pa036"

CMD ["/root/pa036/entrypoint.sh"]

################################################################################

## Before build:
# podman pull fedora:34

## Build:
# podman build . -t databases

## Run as:
# podman run -it databases

################################################################################
# This is no longer needed

# podman run -it --privileged --mount type=bind,source=".",target="/root/pa036" databases

## To initialize PostgreSQL database
# su - postgres -c "/usr/bin/pg_ctl -D /var/lib/pgsql/data -l logfile start"

## Postgres shell
# su - postgres -c "psql"

## To initialize MongoDB database
# mongod --dbpath /var/lib/mongo/data 2>&1 > /dev/null &

## Mongo shell
# mongo
